from settings import *
from component import Component

class Game(Component):
    def __init__(self):
        super().__init__()
        self.set_surface(pygame.Surface((GAME_WIDTH, GAME_HEIGHT)))
        self.set_display_surface(pygame.display.get_surface())
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x,self.surface.get_height()), 1)
        
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.surface.get_width(), y), 1)

        self.get_surface().blit(self.line_surface, (0,0))
    

    def run(self):
        self.surface.fill(GRAY)
        self.draw_grid()
        self.display_surface.blit(self.surface , (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 10)

# class Block(pygame.sprite.Sprite()):
#     def __init__(self):
#         self.image = pygame.surface(CELL_SIZE, CELL_SIZE)
#         self.image.fill = RED
#         self.rect = self.image.get_rect(topleft = (0,0))