"""
Gallery view
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal


class GalleryScene(QWidget):
    """Gallery showing saved sessions"""
    
    new_session_requested = Signal()
    session_selected = Signal(str)
    
    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        # TODO: Setup UI
        # TODO: Add title "Your Visual Sessions"
        # TODO: Add "New Session" button
        # TODO: Add scrollable grid for thumbnails
        pass
    
    def refresh_gallery(self):
        """Refresh gallery with current sessions"""
        # TODO: Load all sessions
        # TODO: Create thumbnail widgets
        # TODO: Display in grid
        pass
