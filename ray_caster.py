import pygame
import time
from pygame import mixer_music
from math import cos, sin, pi, atan2

from button import Button
from gl import *

# base colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SPRITE_BACKGROUND = (146, 156, 207, 255)
SPRITE_BACKGROUND2 = (145, 155, 206, 255)

# dictionary for the numbers in the map and their corresponding texture
textures = {
    '0' : pygame.image.load('img/wall.jpg'),
    '1' : pygame.image.load('img/checkpoint.jpg'),
    '2' : pygame.image.load('img/dark.jpg'),
}

# array for sprites
sprites = {
    'LEVEL1': [
        {
            "x": 75,
            "y": 250,
            "texture" : pygame.image.load('sprites/tile000.png')
        },
        {
            "x": 375,
            "y": 175,
            "texture" : pygame.image.load('sprites/tile001.png')
        },
    ],
    'LEVEL2': [
        {
            "x": 200,
            "y": 225,
            "texture" : pygame.image.load('sprites/tile001.png')
        },
        {
            "x": 275,
            "y": 425,
            "texture" : pygame.image.load('sprites/tile003.png')
        },
    ],
    'LEVEL3': [
        {
            "x": 350,
            "y": 125,
            "texture" : pygame.image.load('sprites/tile002.png')
        },
        {
            "x": 75,
            "y": 125,
            "texture" : pygame.image.load('sprites/tile004.png')
        },
    ]
}


class RayCaster(object):
    # initialize ray caster object
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.active_level = None

        self.map = []
        self.zbuffer = [-float('inf') for z in range(int(self.width))]

        self.block_size = 50
        self.wall_height = 50

        self.step_size = 5

        self.player = {
            "x" : 75,
            "y" : 55,
            "angle" : 90,
            "fov" : 60
        }

    # load map from a .txt file
    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    # clear map for next level
    def clear_map(self):
        self.map = []

    # function for drawing a rectangle
    def draw_rect(self, x, y, texture):
        texture = pygame.transform.scale(texture, (self.block_size, self.block_size))
        rect = texture.get_rect()
        rect = rect.move((x, y))
        self.screen.blit(texture, rect)

    # function for drawing player icon 
    def draw_player_icon(self, color = WHITE):
        rect = (int(self.player['x'] % 61) + 61, int(self.player['y'] % 51) + 51, 5, 5)
        self.screen.fill(color, rect)

    # function for drawing sprites
    def drawSprite(self, sprite, size):
        sprite_dist = ((self.player['x'] - sprite['x']) ** 2 + (self.player['y'] - sprite['y']) ** 2)** 0.5
        sprite_angle = atan2(sprite['y'] - self.player['y'], sprite['x'] - self.player['x'])

        aspect_ratio = sprite["texture"].get_width() / sprite["texture"].get_height()
        sprite_height = (self.height / sprite_dist) * size
        sprite_width = sprite_height * aspect_ratio

        # convertir a radianes
        angle = self.player['angle'] * pi / 180
        fov = self.player['fov'] * pi / 180

        # buscamos el punto inicial para dibujar el sprite
        start_x = int((self.width / 2) + (sprite_angle - angle) * (self.width) / fov - (sprite_width / 2))
        start_y = int((self.height / 2) - (sprite_height / 2))

        for x in range(start_x, int(start_x + sprite_width)):
            for y in range(start_y, int(start_y + sprite_height)):
                if 0 < x < self.width:
                    if self.zbuffer[x - self.width] >= sprite_dist:
                        tx = int( (x - start_x) * sprite["texture"].get_width() / sprite_width)
                        ty = int( (y - start_y) * sprite["texture"].get_height() / sprite_height)

                        tex_color = sprite["texture"].get_at((tx, ty))

                        if (tex_color[3] > 128 and tex_color != SPRITE_BACKGROUND) and (tex_color[3] > 128 and tex_color != SPRITE_BACKGROUND2):
                            self.screen.set_at((x, y), tex_color)
                            self.zbuffer[x - self.width] = sprite_dist

    # function for ray casting
    def cast_ray(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                hit_x = x - i * self.block_size
                hit_y = y - j * self.block_size

                if 1 < hit_x < self.block_size - 1:
                    max_hit = hit_x
                else:
                    max_hit = hit_y

                tx = max_hit / self.block_size

                return dist, self.map[j][i], tx

            dist += 1

    # render function 
    def render(self, al):

        self.active_level = al

        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        # field of view
        for i in range(self.width):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / self.width
            dist, wall_type, tx = self.cast_ray(angle)

            self.zbuffer[i] = dist
            x = i

            h = self.height / (dist * cos((angle - self.player['angle']) * pi / 180 )) * self.wall_height

            start = int(half_height - h / 2)
            end = int(half_height + h / 2)

            image = textures[wall_type]
            tx = int(tx * image.get_width())

            for y in range(start, end):
                ty = (y - start) / (end - start)
                ty = int(ty * image.get_height())
                tex_color = image.get_at((tx, ty))
                self.screen.set_at((x, y), tex_color)
        
        level_sprites = sprites[self.active_level]

        for sprite in level_sprites:
            self.screen.fill(pygame.Color("black"), (sprite['x'], sprite['y'], 3, 3))
            self.drawSprite(sprite, 30)

        # minimap
        screen.fill(pygame.Color("dimgray"), (0, 0, 200, 200))

        for x in range(int(self.player['x'] - 75), int(200 + self.player['x'] - 75), self.block_size):
            for y in range(int(self.player['y'] - 55), int(200 + self.player['y'] - 55), self.block_size):
                
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                try:
                    if self.map[j][i] != ' ':
                        self.draw_rect(int(x - self.player['x'] + 75), int(y - self.player['y'] + 55), textures[self.map[j][i]])
                except:
                    pass

        self.draw_player_icon()

        for i in range(201):
            self.screen.set_at((200, i), BLACK)
            self.screen.set_at((201, i), BLACK)
            self.screen.set_at((0, i), BLACK)
            self.screen.set_at((1, i), BLACK)
            self.screen.set_at((i, 200), BLACK)
            self.screen.set_at((i, 201), BLACK)

# initialize pygame
pygame.init()

# set up screen
screen = pygame.display.set_mode((800, 500))
screen.set_alpha(None)

# initialize Ray Caster
r = RayCaster(screen)
r.load_map('maps/map.txt')

# set up FPS
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# function for updating the FPS
def update_FPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

# load home screen
start_button, quit_button = load_home_screen(screen)
isRunning = home_screen(start_button, quit_button, screen)

# active level
LEVEL = 'LEVEL1'
LOADED = False
CHANGED = False

# variables for continous moving
move_forwards = False
move_backwards = False
move_left = False
move_right = False
turn_right = False
turn_left = False

# initialize in game music
mixer_music.load('soundtrack/LEVEL1.wav')
mixer_music.play(-1)

# cycle for the main game
while isRunning:

    new_x = r.player['x']
    new_y = r.player['y']

    if (new_x > 400 and new_y > 400) or (new_x < 100 and new_y > 400):
        if not CHANGED:
            if LEVEL == 'LEVEL2':
                LEVEL = 'LEVEL3'
            elif LEVEL == 'LEVEL1':
                LEVEL = 'LEVEL2'
            elif LEVEL == 'LEVEL3':
                # end screen
                exit_button, play_button = load_end_screen(screen)
                isRunning = end_screen(exit_button, play_button, screen)

                if isRunning:
                    start_button, quit_button = load_home_screen(screen)
                    isRunning = home_screen(start_button, quit_button, screen)

                    if isRunning:
                        LEVEL = 'LEVEL1'
                        r.clear_map()
            
                        r.player['x'] = 75
                        r.player['y'] = 55
                        r.player['angle'] = 90

                        time.sleep(1)

                        r.load_map('maps/map.txt')
                        
                        mixer_music.load('soundtrack/' + LEVEL + '.wav')
                        mixer_music.play(-1)

                        LOADED = False
                        CHANGED = False

                        move_forwards = False
                        move_backwards = False
                        move_left = False
                        move_right = False
                    
                    else:
                        break

                else:
                    break
            
            CHANGED = True if LEVEL != 'LEVEL1' else False
        
        LOADED = False
            
    if LEVEL != 'LEVEL1':
        if not LOADED:
            r.clear_map()
            
            r.player['x'] = 75
            r.player['y'] = 55
            r.player['angle'] = 90

            time.sleep(1)

            if LEVEL != 'LEVEL2':
                r.load_map('maps/map3.txt')
            else:
                r.load_map('maps/map2.txt')
        
            mixer_music.load('soundtrack/' + LEVEL + '.wav')
            mixer_music.play(-1)

            LOADED = True
        
        CHANGED = False

    for ev in pygame.event.get():
        # manage quitting
        if ev.type == pygame.QUIT:
            isRunning = False

        # x and y variable
        new_x = r.player['x']
        new_y = r.player['y']

        # manage key presses
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                resume_button, quit_button = load_pause_screen()
                isRunning, result = pause_screen(resume_button, quit_button, screen)
                
                if result == 'HOME':
                    start_button, quit_button = load_home_screen(screen)
                    isRunning = home_screen(start_button, quit_button, screen)
                    
                    if isRunning:
                        # initialize in game music
                        mixer_music.load('soundtrack/' + LEVEL + '.wav')
                        mixer_music.play(-1)

                elif result == 'RESUME':
                    isRunning = True
                    
            elif ev.key == pygame.K_w:
                move_forwards = True
            elif ev.key == pygame.K_s:
                move_backwards = True
            elif ev.key == pygame.K_a:
                move_left = True
            elif ev.key == pygame.K_d:
                move_right = True
            elif ev.key == pygame.K_LEFT:
                turn_left = True
            elif ev.key == pygame.K_RIGHT:
                turn_right = True
        
        # manage key releases
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_w:
                move_forwards = False
            elif ev.key == pygame.K_s:
                move_backwards = False
            elif ev.key == pygame.K_a:
                move_left = False
            elif ev.key == pygame.K_d:
                move_right = False
            elif ev.key == pygame.K_LEFT:
                turn_left = False
            elif ev.key == pygame.K_RIGHT:
                turn_right = False

    # manage player's movement
    if move_forwards:
        new_x += cos(r.player['angle'] * pi / 180) * r.step_size
        new_y += sin(r.player['angle'] * pi / 180) * r.step_size
    if move_backwards:
        new_x -= cos(r.player['angle'] * pi / 180) * r.step_size
        new_y -= sin(r.player['angle'] * pi / 180) * r.step_size
    if move_left:
        new_x -= cos((r.player['angle'] + 90) * pi / 180) * r.step_size
        new_y -= sin((r.player['angle'] + 90) * pi / 180) * r.step_size
    if move_right:
        new_x += cos((r.player['angle'] + 90) * pi / 180) * r.step_size
        new_y += sin((r.player['angle'] + 90) * pi / 180) * r.step_size
    if turn_left:
        r.player['angle'] -= 6
    if turn_right:
        r.player['angle'] += 6

    # distance
    i = int(new_x / r.block_size)
    j = int(new_y / r.block_size)

    if r.map[j][i] == ' ':
        r.player['x'] = new_x
        r.player['y'] = new_y

    # fillings for the floor and ceiling
    screen.fill(pygame.Color("gray"))
    screen.fill(pygame.Color("#470684"), (0, 0, r.width, int(r.height / 2))) 
    screen.fill(pygame.Color("dimgray"), (0, int(r.height / 2), int(r.width), int(r.height / 2)))
    r.render(LEVEL)

    # FPS
    screen.fill(pygame.Color("black"), (r.width - 50, 0, r.width, 50))
    screen.blit(update_FPS(), (r.width - 32, 8))
    clock.tick(30)
    
    pygame.display.update()


pygame.quit()
