from settings import *

class Component:
    def __init__(self):
        self.surface = None
        self.display_surface = None

    def set_surface(self, surface):
        self.surface = surface

    def set_display_surface(self, display_surface):
        self.display_surface = display_surface

    def get_surface(self):
        return self.surface
    
    def get_display_surface(self):
        return self.display_surface

    def run(self):
        self.display_surface.blit(self.surface, self.rect)