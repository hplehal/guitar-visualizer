"""
Base effect classes
"""

from PySide6.QtGui import QPainter, QColor


class Effect:
    """Base class for visual effects"""
    
    def __init__(self, x: float, y: float, color: QColor):
        self.x = x
        self.y = y
        self.color = color
        self.age = 0.0
        self.lifetime = 3.0
        self.is_expired = False
    
    def update(self, dt: float):
        """Update effect state"""
        # TODO: Increment age
        # TODO: Mark as expired if lifetime exceeded
        pass
    
    def render(self, painter: QPainter):
        """Render the effect"""
        # TODO: Override in subclasses
        pass


class EffectManager:
    """Manages all active effects"""
    
    def __init__(self):
        self.effects = []
    
    def add_effect(self, effect: Effect):
        """Add a new effect"""
        # TODO: Add to list
        # TODO: Limit max effects
        pass
    
    def update(self, dt: float):
        """Update all effects"""
        # TODO: Update each effect
        # TODO: Remove expired effects
        pass
    
    def render(self, painter: QPainter):
        """Render all effects"""
        # TODO: Render each effect
        pass
