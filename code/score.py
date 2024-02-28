from settings import *
from component import Component

class Score(Component):
    
    def __init__(self):
        super().__init__()
        self.set_surface(pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING)))
        """add rect to component class"""
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.set_display_surface(pygame.display.get_surface())