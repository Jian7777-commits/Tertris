from settings import *
from component import Component
from os.path import join
class Score(Component):
    
    def __init__(self):
        super().__init__()
        self.set_surface(pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING)))
        """add rect to component class"""
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))

        self.font = pygame.font.Font(join('./', 'graphics','Russo_One.ttf'),30)
        self.increment_height = self.surface.get_height() / 3

        self.set_display_surface(pygame.display.get_surface())

        self.score = 0
        self.level = 1
        self.lines = 0


    def display_text(self, pos, text):
        text_surface = self.font.render(f"{text[0]} : {text[1]}", True, LINE_COLOR)
        text_rect = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill(GRAY)
        for i, text in enumerate([('Score', self.score), ('Level', self.level), ('Lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            self.display_text((x,y), text)

        self.display_surface.blit(self.surface, self.rect)