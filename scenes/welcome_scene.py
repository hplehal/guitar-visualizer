"""
Welcome screen
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal


class WelcomeScene(QWidget):
    """Welcome screen with greeting"""
    
    finished = Signal()
    
    def __init__(self):
        super().__init__()
        # TODO: Setup UI with "Welcome, Julian" text
        # TODO: Style with dark background
        pass
    
    def start_animation(self):
        """Start fade in/out animation"""
        # TODO: Fade in
        # TODO: Hold for 2 seconds
        # TODO: Fade out
        # TODO: Emit finished signal
        pass
