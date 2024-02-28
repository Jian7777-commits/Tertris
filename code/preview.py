from settings import *
from component import Component

class Preview(Component):
    def __init__(self):
        super().__init__()
        self.set_surface(pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION)))
        """add rect to component class"""
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING))
        self.set_display_surface(pygame.display.get_surface())