#!/usr/bin/env python3
"""
System Resource Monitor - Main Entry Point
Launch the resource monitor application
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui import main

if __name__ == '__main__':
    main()
