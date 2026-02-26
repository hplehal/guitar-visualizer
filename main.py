#!/usr/bin/env python3
"""
Guitar Visual Art Generator
Main entry point
"""

import sys
from PySide6.QtWidgets import QApplication
from core.app import GuitarVisualApp


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Guitar Visual Art")
    
    window = GuitarVisualApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
