import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Packman')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((0, 0, 0))
        scr.blit(bg, (0, 0))


class Map:
        def __init__(self, h):
            self.map = [None for i in range(h)]
            txt = open('./resources/map.txt', 'r')
            for x in range(h):
                a = txt.readline()
                a = a.rstrip()
                self.map[x] = list(a.split('.'))

        def get(self, x, y):
                return self.map[x][y]

class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))

    def checkwall(self, x, y, direction):
        a = self.x
        b = self.y
        if self.direction == 1:
            a += self.velocity
        elif self.direction == 2:
            b += self.velocity
        elif self.direction == 3:
            a -= self.velocity
        elif self.direction == 4:
            b -= self.velocity
        a = int(a)
        b = int(b)
        if map.get(a, b) == 'w':
            return True
        else:
            return False


class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0

class Ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Ghost, self).game_tick()

        if self.checkwall(self.x, self.y, self.direction):
            self.direction = random.randint(1, 4)
        else:
            if self.tick % 20 == 0 or self.direction == 0:
                self.direction = random.randint(1, 4)
            if self.direction == 1:
                self.x += self.velocity
                if self.x >= self.map_size-1:
                    self.x = self.map_size-1
                    self.direction = random.randint(1, 4)
            elif self.direction == 2:
                self.y += self.velocity
                if self.y >= self.map_size-1:
                    self.y = self.map_size-1
                    self.direction = random.randint(1, 4)
            elif self.direction == 3:
                self.x -= self.velocity
                if self.x <= 0:
                    self.x = 0
                    self.direction = random.randint(1, 4)
            elif self.direction == 4:
                self.y -= self.velocity
                if self.y <= 0:
                    self.y = 0
                    self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)


class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Pacman, self).game_tick()

        if self.checkwall(self.x, self.y, self.direction):
            self.direction = 0
        else:
            if self.direction == 1:
                self.x += self.velocity
                if self.x >= self.map_size-1:
                    self.x = self.map_size-1
            elif self.direction == 2:
                self.y += self.velocity
                if self.y >= self.map_size-1:
                    self.y = self.map_size-1
            elif self.direction == 3:
                self.x -= self.velocity
                if self.x <= 0:
                    self.x = 0
            elif self.direction == 4:
                self.y -= self.velocity
                if self.y <= 0:
                    self.y = 0

        self.set_coord(self.x, self.y)

def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
                pacman.image = pygame.image.load('./resources/pacman2.png')
            elif event.key == K_RIGHT:
                packman.direction = 1
                pacman.image = pygame.image.load('./resources/pacman.png')
            elif event.key == K_UP:
                packman.direction = 4
                pacman.image = pygame.image.load('./resources/pacman3.png')
            elif event.key == K_DOWN:
                packman.direction = 2
                pacman.image = pygame.image.load('./resources/pacman1.png')
            elif event.key == K_SPACE:
                packman.direction = 0


class Dot(GameObject):

    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/facebook.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0
        self.eaten = False

    def game_tick(self):
        super(Dot, self).game_tick()
        if int(pacman.x) == self.x and int(pacman.y) == self.y:
            self.eaten = True
            self.image = pygame.image.load('./resources/vk.png')


if __name__ == '__main__':
    win = None
    init_window()
    tile_size = 32
    map_size = 16
    map = Map(16)
    ghosts = []
    for x in range(map_size):
        for y in range(map_size):
            if map.get(x,y) == 'g':
                ghosts.append(Ghost(x, y, tile_size, map_size))
    pacman = Pacman(3, 1, tile_size, map_size)
    walls = []
    for x in range(map_size):
        for y in range(map_size):
            if map.get(x,y) == 'w':
                walls.append(Wall(x, y, tile_size, map_size))
    dots = []
    for x in range(map_size):
        for y in range(map_size):
            if map.get(x,y) == 'd':
                dots.append(Dot(x, y, tile_size, map_size))
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        for ghost in ghosts:
            ghost.game_tick()
        pacman.game_tick()
        for dot in dots:
            dot.game_tick()
        draw_background(screen, background)
        pacman.draw(screen)
        for w in walls:
            w.draw(screen)
        for dot in dots:
            dot.draw(screen)
        i = 0
        for dot in dots:
            if not dot.eaten:
                i += 1
        if i == 0:
            win = True
            break
        for ghost in ghosts:
            if int(ghost.x) == int(pacman.x) and int(ghost.y) == int(pacman.y):
                win = False
                break
        pygame.display.update()

    if win == True:
        print('Good game!')
    else:
        print(':(')

