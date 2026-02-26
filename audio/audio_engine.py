"""
Audio capture and processing
"""

from PySide6.QtCore import QThread, Signal, QObject


class AudioProcessor(QObject):
    """Audio processor running in separate thread"""
    
    audio_analyzed = Signal(dict)
    
    def __init__(self):
        super().__init__()
        # TODO: Initialize pitch detector
        
        # TODO: Initialize technique detector
        pass
    
    def start(self):
        """Start audio capture"""
        # TODO: Start sounddevice stream
        # TODO: Process incoming audio
        pass
    
    def stop(self):
        """Stop audio capture"""
        # TODO: Stop stream
        pass
    
    def _process_audio(self, audio_data):
        """Process audio and detect pitch/techniques"""
        # TODO: Detect pitch
        # TODO: Detect technique
        # TODO: Emit results
        pass


class AudioEngine:
    """Main audio engine"""
    
    def __init__(self, visual_widget):
        self.visual_widget = visual_widget
        # TODO: Create processor thread
        # TODO: Connect signals
        pass
    
    def start(self):
        """Start audio engine"""
        # TODO: Start thread
        pass
    
    def stop(self):
        """Stop audio engine"""
        # TODO: Stop thread
        pass
