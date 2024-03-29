from settings import *
from component import Component
from random import choice
from timer import Timer
from sys import exit
from os.path import join

class Game(Component):
    def __init__(self, get_next_shape, update_score):
        #general attr
        super().__init__()
        self.set_surface(pygame.Surface((GAME_WIDTH, GAME_HEIGHT)))
        self.set_display_surface(pygame.display.get_surface())
        """add rect to component class"""
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        self.get_next_shape = get_next_shape
        self.update_score = update_score
        
        #line attr
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        
        #create a Tetromino
        self.field_data = [[0 for x in range(COLUMNS)]for y in range(ROWS)]
        
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())), 
            self.sprites, 
            self.create_tetromino,
            self.field_data)

        #timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move' : Timer(MOVE_WAIT_TIME),
            'rotate' : Timer(ROTATE_WAIT_TIME)
        }

        self.timers["vertical move"].activate()

        #score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= .75
            self.down_speed_faster = self.down_speed  * 0.3
            self.timers['vertical move'].duration = self.down_speed

        self.update_score(self.current_lines, self.current_score, self.current_level)
    def check_gameover(self):
        for block in self.tetromino.block:
            if block.pos.y < 0:
                exit()

    def create_tetromino(self):
        self.check_gameover()
        self.check_complete_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(), 
            self.sprites, 
            self.create_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x,self.surface.get_height()), 1)
        
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.surface.get_width(), y), 1)

        self.get_surface().blit(self.line_surface, (0,0))
    
    def input_handler(self):
        keys = pygame.key.get_pressed()
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster
        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def check_complete_rows(self):
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                for block in self.field_data[delete_row]:
                    block.kill()

                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            self.field_data = [[0 for x in range(COLUMNS)]for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.calculate_score(len(delete_rows))



    def run(self):

        self.timer_update()
        self.sprites.update()
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface , (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 3)

        self.input_handler()

class Tetromino():
    def __init__(self, shape, group, create_tetromino, field_data):
        #setup
        self.shape = shape
        self.block_position = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_tetromino = create_tetromino
        self.field_data = field_data
        #audio
        self.audio = pygame.mixer.Sound(join('./','sound','landing.wav'))

        #store as shape a list
        self.block = [Block(group, pos, self.color) for pos in self.block_position]
    
    def horizontal_collision_handler(self, blocks, amount):
        collision_list = [blocks.horizontal_collide(int(blocks.pos.x + amount), self.field_data) for  blocks in self.block]
        return True if any(collision_list) else False

    def vertical_collision_handler(self, blocks, amount):
        collision_list = [blocks.vertical_collide(int(blocks.pos.y + amount), self.field_data) for  blocks in self.block]
        return True if any(collision_list) else False


    def move_down(self):
        if not self.vertical_collision_handler(self.block, 1):
            for block in self.block:
                block.pos.y += 1
        else:
            for block in self.block:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.audio.play()
            self.create_tetromino()

    def move_horizontal(self, amount):
        if not self.horizontal_collision_handler(self.block, amount):
            for block in self.block:
                block.pos.x += amount

    def rotate(self):
        if self.shape != 'O':
            pivot_pos = self.block[0].pos
            new_block_pos = [block.rotate(pivot_pos) for block in self.block]

            for pos in new_block_pos:
                if pos.x >= COLUMNS or pos.x < 0:
                    return

                if pos.y > ROWS:
                    return
                
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
            
            for i, block in enumerate(self.block):
                block.pos = new_block_pos[i]



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

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if not y < ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
    
    def rotate(self, pivot_pos):
        distance = self.pos - pivot_pos
        rotated = distance.rotate(90)
        new_pos = pivot_pos + rotated

        return new_pos

