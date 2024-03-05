from settings import *
from component import Component
from pygame.image import load
from os import path

class Preview(Component):
    def __init__(self):
        super().__init__()
        self.set_surface(pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION)))
        """add rect to component class"""
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING))
        self.set_display_surface(pygame.display.get_surface())

        self.shape_surfaces = {shape : load(path.join("./","graphics",f"{shape}.png")).convert_alpha()  for shape in TETROMINOS.keys()}
        
        self.shape_preview_height = self.surface.get_height() / 3

    def display_pieces(self, shapes):
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            x = self.surface.get_width() / 2
            y = self.shape_preview_height / 2 + i * self.shape_preview_height
            rect = shape_surface.get_rect(center = (x,y))
            self.surface.blit(shape_surface, rect)
            

    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)    
