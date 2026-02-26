"""
Note to color mapping
"""

from PySide6.QtGui import QColor


class ColorMapper:
    """Maps notes to colors"""
    
    def __init__(self):
        # TODO: Setup note-to-hue mapping (12 notes = 30° apart)
        pass
    
    def note_to_color(self, note_number: int, amplitude: float = 0.5) -> QColor:
        """
        Convert MIDI note to color
        
        Args:
            note_number: MIDI note (0-127)
            amplitude: Volume (0-1)
        
        Returns:
            QColor
        """
        # TODO: Get note within octave (0-11)
        # TODO: Map to hue on color wheel
        # TODO: Set saturation and brightness
        # TODO: Return QColor in HSV space
        pass
