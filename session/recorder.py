"""
Session recorder
"""

from PySide6.QtCore import QObject


class SessionRecorder(QObject):
    """Records audio and video"""
    
    def __init__(self, session_id, project_manager, audio_engine, visual_widget):
        super().__init__()
        self.session_id = session_id
        self.project_manager = project_manager
        self.audio_engine = audio_engine
        self.visual_widget = visual_widget
    
    def start_recording(self):
        """Start recording"""
        # TODO: Setup video writer
        # TODO: Start capturing frames
        pass
    
    def stop_recording(self):
        """Stop and save"""
        # TODO: Save audio to WAV
        # TODO: Finalize video
        # TODO: Generate thumbnail
        # TODO: Update metadata
        pass
