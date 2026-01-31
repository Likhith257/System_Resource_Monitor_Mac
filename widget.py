#!/usr/bin/env python3
"""
System Resource Monitor - Menu Bar Widget Entry Point
Launch the lightweight menu bar widget
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from menubar_widget import main

if __name__ == '__main__':
    main()
