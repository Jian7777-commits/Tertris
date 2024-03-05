from settings import *
from sys import exit
from os.path import join

from game import Game
from score import Score
from preview import Preview
from random import choice
from collections import deque

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        #shapes
        self.next_shapes = deque([choice(list(TETROMINOS.keys())) for shape in range(3)])
        

        #components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

        self.audio = pygame.mixer.Sound(join('./','sound', 'music.wav'))
        self.audio.play(-1)

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        add_shape = choice(list(TETROMINOS.keys()))
        while add_shape in self.next_shapes:
            add_shape = choice(list(TETROMINOS.keys()))
        if add_shape not in self.next_shapes:
            self.next_shapes.append(add_shape)
        next_shape = self.next_shapes.popleft()
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #display
            self.display_surface.fill(GRAY)
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)
            
            pygame.display.update()
            self.clock.tick()

if __name__ == '__main__':
    main = Main()
    main.run()
