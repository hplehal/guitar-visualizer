"""
Main visualizer scene
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal


class VisualizerScene(QWidget):
    """Recording/playback scene"""
    
    session_ended = Signal()
    
    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        # TODO: Setup UI with visual canvas
        # TODO: Add control bar with record/stop button
        # TODO: Add back button
        pass
    
    def start_new_session(self):
        """Start a new recording session"""
        # TODO: Create new session
        # TODO: Initialize audio engine
        # TODO: Initialize recorder
        pass
    
    def _toggle_recording(self):
        """Start or stop recording"""
        # TODO: Implement recording toggle
        pass
