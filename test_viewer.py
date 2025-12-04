#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Documentation Viewer
Run this to test the viewer standalone
"""

from tkinter import *
from tkinter import ttk
from markdown_viewer import open_documentation_viewer

def main():
    """Test the documentation viewer"""
    root = Tk()
    root.title("Documentation Viewer Test")
    root.geometry("400x300")
    
    # Create test UI
    frame = ttk.Frame(root, padding=40)
    frame.pack(fill=BOTH, expand=True)
    
    ttk.Label(
        frame, 
        text="Documentation Viewer Test",
        font=('Arial', 14, 'bold')
    ).pack(pady=20)
    
    ttk.Label(
        frame,
        text="Click the button below to open the viewer,\nor press F1 as you would in BalrogNPC.",
        justify=CENTER
    ).pack(pady=10)
    
    def open_viewer():
        open_documentation_viewer(root)
    
    ttk.Button(
        frame,
        text="Open Documentation Viewer",
        command=open_viewer
    ).pack(pady=20)
    
    ttk.Label(
        frame,
        text="Press F1",
        font=('Arial', 10, 'italic'),
        foreground='#666666'
    ).pack()
    
    # Bind F1
    root.bind('<F1>', lambda e: open_viewer())
    
    # Status
    status = ttk.Label(root, text="Ready - Press F1 or click button", relief=SUNKEN)
    status.pack(side=BOTTOM, fill=X, padx=5, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    print("Starting Documentation Viewer Test...")
    print("Press F1 or click button to open viewer")
    main()
