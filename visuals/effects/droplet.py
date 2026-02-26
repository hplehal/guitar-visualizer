"""
Water droplet effect for hammer-ons
"""

from PySide6.QtGui import QPainter, QColor
from visuals.effects.base_effect import Effect


class WaterDroplet(Effect):
    """Small droplet splash"""
    
    def __init__(self, x: float, y: float, color: QColor):
        super().__init__(x, y, color)
        # TODO: Set properties
        pass
    
    def render(self, painter: QPainter):
        """Render the droplet"""
        # TODO: Implement splash effect
        pass


# Similarly create:
# - RippleEffect (ripple.py) - for vibrato
# - GradientSlide (gradient_slide.py) - for slides
