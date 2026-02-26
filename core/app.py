"""
Main application window
"""

from PySide6.QtWidgets import QMainWindow, QStackedWidget
from scenes.welcome_scene import WelcomeScene
from scenes.gallery_scene import GalleryScene
from scenes.visualizer_scene import VisualizerScene


class GuitarVisualApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guitar Visual Art")
        self.setMinimumSize(1024, 768)
        
        # TODO: Initialize project manager
        
        # TODO: Create stacked widget for scenes
        
        # TODO: Initialize scenes
        
        # TODO: Start with welcome screen
        pass
    
    def show_welcome(self):
        """Show welcome screen"""
        # TODO: Implement
        pass
    
    def show_gallery(self):
        """Show gallery screen"""
        # TODO: Implement
        pass
    
    def start_new_session(self):
        """Start a new recording session"""
        # TODO: Implement
        pass
