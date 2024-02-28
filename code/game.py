from settings import *
from component import Component
from random import choice

class Game(Component):
    def __init__(self):
        #general attr
        super().__init__()
        self.set_surface(pygame.Surface((GAME_WIDTH, GAME_HEIGHT)))
        self.set_display_surface(pygame.display.get_surface())
        """add rect to component class"""
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()
        
        #line attr
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)
        
        #create a Tetromino
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), group=self.sprites)
    



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
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface , (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 3)

class Tetromino():
    def __init__(self, shape, group):
        #setup
        self.block_position = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        #store as shape a list
        self.block = [Block(group, pos, self.color) for pos in self.block_position]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        #general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        #position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft = (x,y))
