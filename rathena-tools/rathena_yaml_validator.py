#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rAthena YAML Database Validator

Validates rAthena YAML database files (quest_db.yml, item_db.yml, mob_db.yml, etc.)
for syntax errors, schema compliance, and reference integrity.
"""

import os
import re

# Try to import yaml, provide fallback if not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("[INFO] PyYAML not available. Using lightweight fallback parser for basic validation.")


def _simple_yaml_parse(yaml_text):
    """
    Lightweight YAML parser for rAthena databases when PyYAML is not available.
    
    Handles only the simple, predictable structure of rAthena YAML files:
    - Key: Value pairs
    - Lists (- items)
    - Nested dictionaries (indentation-based)
    - Simple strings, integers, booleans
    
    Does NOT handle: anchors, aliases, complex multiline strings, flow style
    
    Returns: dict representing the parsed YAML, or raises exception on error
    """
    lines = yaml_text.split('\n')
    root = {}
    stack = [(root, -1)]  # (current_dict, indent_level)
    current_list = None
    current_list_indent = -1
    
    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        
        # Calculate indentation (spaces only for simplicity)
        indent = len(line) - len(line.lstrip(' '))
        
        # Check for tabs (rAthena YAML uses spaces)
        if '\t' in line[:indent]:
            raise ValueError(f"Line {line_num}: Use spaces for indentation, not tabs")
        
        # Handle list items (starts with -)
        if stripped.startswith('- '):
            # List item
            item_content = stripped[2:].strip()
            
            # Close any deeper list
            if current_list is not None and indent <= current_list_indent:
                current_list = None
                current_list_indent = -1
            
            # Pop stack to correct level
            while stack and stack[-1][1] >= indent:
                stack.pop()
            
            if not stack:
                raise ValueError(f"Line {line_num}: Invalid indentation")
            
            parent_dict, parent_indent = stack[-1]
            
            # Initialize list in parent if needed
            # Find the last key added to parent
            if parent_dict:
                last_key = list(parent_dict.keys())[-1] if parent_dict else None
                if last_key and not isinstance(parent_dict[last_key], list):
                    parent_dict[last_key] = []
                    current_list = parent_dict[last_key]
                    current_list_indent = indent
                elif last_key:
                    current_list = parent_dict[last_key]
                    current_list_indent = indent
            
            # Parse item content
            if ':' in item_content:
                # List item is a dict
                new_dict = {}
                key, value = item_content.split(':', 1)
                key = key.strip()
                value = value.strip()
                new_dict[key] = _parse_value(value)
                if current_list is not None:
                    current_list.append(new_dict)
                    stack.append((new_dict, indent))
                else:
                    raise ValueError(f"Line {line_num}: List item without parent list")
            else:
                # Simple list item
                if current_list is not None:
                    current_list.append(_parse_value(item_content))
                else:
                    raise ValueError(f"Line {line_num}: List item without parent list")
        
        # Handle key: value pairs
        elif ':' in stripped:
            # Pop stack to correct indentation level
            while stack and stack[-1][1] >= indent:
                stack.pop()
            
            if not stack:
                raise ValueError(f"Line {line_num}: Invalid indentation")
            
            parent_dict, parent_indent = stack[-1]
            
            # Parse key: value
            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if value:
                # Inline value
                parent_dict[key] = _parse_value(value)
            else:
                # Value on next line or nested structure
                parent_dict[key] = {}
                stack.append((parent_dict[key], indent))
        
        else:
            raise ValueError(f"Line {line_num}: Invalid YAML syntax: {stripped}")
    
    return root


def _parse_value(value_str):
    """Parse a YAML value string into Python type"""
    value_str = value_str.strip()
    
    # Remove quotes from strings
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    
    # Boolean
    if value_str.lower() in ('true', 'yes', 'on'):
        return True
    if value_str.lower() in ('false', 'no', 'off'):
        return False
    
    # Null
    if value_str.lower() in ('null', '~', ''):
        return None
    
    # Integer
    try:
        return int(value_str)
    except ValueError:
        pass
    
    # Float
    try:
        return float(value_str)
    except ValueError:
        pass
    
    # Default to string
    return value_str


class RathenaYAMLValidator:
    """Validator for rAthena YAML database files"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.suggestions = []
        self.fixable_issues = []
        
        # Cache for reference data (loaded once)
        self._mob_names = None
        self._item_names = None
        self._map_names = None
    
    def validate(self, yaml_text):
        """
        Validate YAML database file content
        
        Returns: (errors, warnings, suggestions)
        """
        self.errors = []
        self.warnings = []
        self.suggestions = []
        self.fixable_issues = []
        
        if not yaml_text.strip():
            self.errors.append((0, 0, "YAML file is empty"))
            return self.errors, self.warnings, self.suggestions
        
        # Phase 1: Parse YAML syntax
        try:
            if YAML_AVAILABLE:
                # Use PyYAML for full YAML parsing
                data = yaml.safe_load(yaml_text)
            else:
                # Use simple fallback parser
                self.suggestions.append((0, 0, "Using fallback parser (PyYAML recommended for full validation)"))
                data = _simple_yaml_parse(yaml_text)
        except Exception as e:
            # Handle both PyYAML errors and fallback parser errors
            if YAML_AVAILABLE and hasattr(e, 'problem_mark'):
                # PyYAML error
                line = getattr(e, 'problem_mark', None)
                line_num = line.line + 1 if line else 0
                problem = getattr(e, 'problem', str(e))
                self.errors.append((line_num, 0, f"YAML Syntax Error: {problem}"))
            else:
                # Fallback parser error or other exception
                self.errors.append((0, 0, str(e)))
            return self.errors, self.warnings, self.suggestions
        
        if data is None:
            self.errors.append((0, 0, "YAML file parsed but contains no data"))
            return self.errors, self.warnings, self.suggestions
        
        # Phase 2: Validate structure
        self._validate_structure(data, yaml_text)
        
        # Phase 3: Validate based on database type
        db_type = self._detect_database_type(data)
        if db_type == 'QUEST_DB':
            self._validate_quest_db(data, yaml_text)
        elif db_type == 'ITEM_DB':
            self._validate_item_db(data, yaml_text)
        elif db_type == 'MOB_DB':
            self._validate_mob_db(data, yaml_text)
        else:
            self.warnings.append((0, 0, f"Unknown database type: {db_type}. Limited validation performed."))
        
        return self.errors, self.warnings, self.suggestions
    
    def _detect_database_type(self, data):
        """Detect the type of database from Header"""
        if not isinstance(data, dict):
            return None
        
        header = data.get('Header', {})
        if isinstance(header, dict):
            return header.get('Type', 'UNKNOWN')
        
        return 'UNKNOWN'
    
    def _validate_structure(self, data, yaml_text):
        """Validate basic YAML structure (Header, Body, Footer)"""
        if not isinstance(data, dict):
            self.errors.append((0, 0, "Root element must be a dictionary"))
            return
        
        # Check required sections
        if 'Header' not in data:
            self.errors.append((0, 0, "Missing required section: Header"))
        else:
            self._validate_header(data['Header'], yaml_text)
        
        if 'Body' not in data:
            self.warnings.append((0, 0, "Missing Body section (database has no entries)"))
        else:
            if not isinstance(data['Body'], list):
                self.errors.append((0, 0, "Body must be a list of entries"))
        
        # Footer is optional but should be validated if present
        if 'Footer' in data:
            self._validate_footer(data['Footer'], yaml_text)
    
    def _validate_header(self, header, yaml_text):
        """Validate Header section"""
        if not isinstance(header, dict):
            self.errors.append((0, 0, "Header must be a dictionary"))
            return
        
        # Required fields
        if 'Type' not in header:
            self.errors.append((0, 0, "Header.Type is required"))
        
        if 'Version' not in header:
            self.warnings.append((0, 0, "Header.Version is recommended"))
        elif not isinstance(header['Version'], int):
            self.warnings.append((0, 0, "Header.Version should be an integer"))
    
    def _validate_footer(self, footer, yaml_text):
        """Validate Footer section"""
        if not isinstance(footer, dict):
            self.warnings.append((0, 0, "Footer should be a dictionary"))
            return
        
        # Validate Imports if present
        if 'Imports' in footer:
            imports = footer['Imports']
            if not isinstance(imports, list):
                self.warnings.append((0, 0, "Footer.Imports should be a list"))
            else:
                for idx, imp in enumerate(imports):
                    if not isinstance(imp, dict):
                        continue
                    if 'Path' not in imp:
                        self.warnings.append((0, 0, f"Import {idx + 1}: Missing Path"))
    
    def _validate_quest_db(self, data, yaml_text):
        """Validate quest_db.yml specific schema"""
        body = data.get('Body', [])
        if not isinstance(body, list):
            return
        
        for idx, entry in enumerate(body):
            if not isinstance(entry, dict):
                continue
            
            entry_num = idx + 1
            
            # Required: Id
            if 'Id' not in entry:
                self.errors.append((0, 0, f"Quest entry {entry_num}: Missing required field 'Id'"))
            elif not isinstance(entry['Id'], int):
                self.warnings.append((0, 0, f"Quest entry {entry_num}: Id should be an integer"))
            
            # Required: Title
            if 'Title' not in entry:
                self.errors.append((0, 0, f"Quest entry {entry_num}: Missing required field 'Title'"))
            elif not isinstance(entry['Title'], str):
                self.warnings.append((0, 0, f"Quest entry {entry_num}: Title should be a string"))
            
            # Optional: TimeLimit (should be non-negative)
            if 'TimeLimit' in entry:
                time_limit = entry['TimeLimit']
                if not isinstance(time_limit, int):
                    self.warnings.append((0, 0, f"Quest entry {entry_num}: TimeLimit should be an integer"))
                elif time_limit < 0:
                    self.errors.append((0, 0, f"Quest entry {entry_num}: TimeLimit cannot be negative"))
            
            # Validate Targets
            if 'Targets' in entry:
                self._validate_quest_targets(entry['Targets'], entry_num)
            
            # Validate Drops
            if 'Drops' in entry:
                self._validate_quest_drops(entry['Drops'], entry_num)
    
    def _validate_quest_targets(self, targets, quest_num):
        """Validate quest targets"""
        if not isinstance(targets, list):
            self.warnings.append((0, 0, f"Quest {quest_num}: Targets should be a list"))
            return
        
        for idx, target in enumerate(targets):
            if not isinstance(target, dict):
                continue
            
            target_num = idx + 1
            
            # Mob name (optional but common)
            if 'Mob' in target:
                mob_name = target['Mob']
                if not isinstance(mob_name, str):
                    self.warnings.append((0, 0, f"Quest {quest_num}, Target {target_num}: Mob should be a string"))
                # TODO: Validate against mob_db when reference loading is implemented
            
            # Count (should be positive integer)
            if 'Count' in target:
                count = target['Count']
                if not isinstance(count, int):
                    self.warnings.append((0, 0, f"Quest {quest_num}, Target {target_num}: Count should be an integer"))
                elif count < 0:
                    self.errors.append((0, 0, f"Quest {quest_num}, Target {target_num}: Count cannot be negative"))
            
            # Id (unique target index)
            if 'Id' in target:
                target_id = target['Id']
                if not isinstance(target_id, int):
                    self.warnings.append((0, 0, f"Quest {quest_num}, Target {target_num}: Id should be an integer"))
                elif target_id < 1:
                    self.errors.append((0, 0, f"Quest {quest_num}, Target {target_num}: Id must be positive"))
    
    def _validate_quest_drops(self, drops, quest_num):
        """Validate quest drops"""
        if not isinstance(drops, list):
            self.warnings.append((0, 0, f"Quest {quest_num}: Drops should be a list"))
            return
        
        for idx, drop in enumerate(drops):
            if not isinstance(drop, dict):
                continue
            
            drop_num = idx + 1
            
            # Mob (0 = all monsters)
            if 'Mob' in drop:
                mob = drop['Mob']
                if not isinstance(mob, (int, str)):
                    self.warnings.append((0, 0, f"Quest {quest_num}, Drop {drop_num}: Mob should be int or string"))
            
            # Item (required)
            if 'Item' not in drop:
                self.errors.append((0, 0, f"Quest {quest_num}, Drop {drop_num}: Missing required field 'Item'"))
            # TODO: Validate against item_db when reference loading is implemented
            
            # Rate (should be 0-10000)
            if 'Rate' in drop:
                rate = drop['Rate']
                if not isinstance(rate, int):
                    self.warnings.append((0, 0, f"Quest {quest_num}, Drop {drop_num}: Rate should be an integer"))
                elif rate < 0:
                    self.errors.append((0, 0, f"Quest {quest_num}, Drop {drop_num}: Rate cannot be negative"))
                elif rate > 10000:
                    self.warnings.append((0, 0, f"Quest {quest_num}, Drop {drop_num}: Rate exceeds 10000 (>100%)"))
            
            # Count (should be positive)
            if 'Count' in drop:
                count = drop['Count']
                if not isinstance(count, int):
                    self.warnings.append((0, 0, f"Quest {quest_num}, Drop {drop_num}: Count should be an integer"))
                elif count < 1:
                    self.errors.append((0, 0, f"Quest {quest_num}, Drop {drop_num}: Count must be at least 1"))
    
    def _validate_item_db(self, data, yaml_text):
        """Validate item_db.yml specific schema"""
        # TODO: Implement item_db validation
        self.suggestions.append((0, 0, "Item database validation not yet implemented"))
    
    def _validate_mob_db(self, data, yaml_text):
        """Validate mob_db.yml specific schema"""
        # TODO: Implement mob_db validation
        self.suggestions.append((0, 0, "Monster database validation not yet implemented"))


# Standalone validation function for easy integration
def validate_yaml_content(yaml_text):
    """
    Validate YAML database file content
    
    Args:
        yaml_text: String content of YAML file
    
    Returns:
        Tuple of (errors, warnings, suggestions)
        Each is a list of tuples: (line_number, column, message)
    """
    validator = RathenaYAMLValidator()
    return validator.validate(yaml_text)
