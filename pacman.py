import sys
import pygame
import random
from math import floor
from pygame.locals import *

class GameObject(pygame.sprite.Sprite):
      def __init__(self, tile_size, map_size, kind = None, status = True, identity, img, x, y):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.image.load(img)
          self.screen_rect = None 
          self.x = x
          self.y = y
          self.tile_size = tile_size
          self.map_size = map_size
          self.set_coord(x,y)
          self.status = status
          self.type = kind
          self.tick = 0
  
      
      def set_coord(self, x, y):
          self.x = x
          self.y = y
          self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size)
     
      
      def get_x(self):
          return self.x 

      def get_y(self):
          return self.y

      def set_status(self, newstatus):
          self.status = newstatus
      
      def set_type(self, newtype):
          self.type = newtype
      
      def get_status(self):
          return self.status
 
      def get_type(self):
          return self.type
    
      def draw(self, scr):
          scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))
      
      def iterate(self):
          self.tick += 1


class Ghost(GameObject):
      def __init__(self, x, y, tile_size, map_size):
          GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
          self.direction = 0 
          self.velocity = 4.0 / 10.0 
          self.damage = 1
          self.set_type('Ghost')
      
      def get_damage(self): 
          return self.damage

      def logic(world):
          x =  super(Ghost, self).get_x()
          y =  super(Ghost, self).get_y()
          super(Ghost, self).iterate()
          for obj in world.get_map()[x][y]:
              if obj.get_type() == 'Pacman':
                 obj.pain(self.get_damage())
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
                 world.move(self, x, y, self.get_x(), self.get_y())

                 

class Candy(GameObject):
      def __init__(self, x, y, tile_size, map_size):
         GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
         self.set_type('Candy')

      def eaten(self):
          super(Candy, self).set_status(False)
      
      def logic(self, world):
          pass

class Wall(GameObject):
      def __init__(self, x, y, tile_size, map_size):
         GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
         self.set_type('Wall')
      
      def logic(self, world):
          pass

class Pacman(GameObject):
        def __init__(self, x, y, tile_size, map_size):
                GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
                self.direction = 0               
                self.velocity = 4.0 / 10.0  
                self.set_type('Pacman')
      
        def logic(self, world):                     
                
                x =  super(Ghost, self).get_x()
                y =  super(Ghost, self).get_y()
                super(Ghost, self).iterate()
                for obj in world.get_map()[x][y]:
                    if obj.get_type() == 'Candy':
                       obj.eaten()

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

                world.move(self, x, y, self.get_x(), self.get_y())
                self.set_coord(self.x, self.y)

class Game:
      def __init__(self, config):
          self.map = parse(config) 
      
      
      def get_map(self):
          return self.map
      
      def move(self, who, from_x, from_y, to_x, to_y):
          self.map[to_x][to_y].append(who)
          for i in range(len(self.map[from_x][from_y])):
              if self.map[from_x][from_y][i] is who:
                 self.map[from_x][from_y].pop(i)
      
      def find_pacman(self):
          for x in self.map:
              for y in x:
                  for obj in y:
                      if obj.get_type() == 'Pacman':
                         return obj

      def check_candy(self):
          for x in self.map:
              for y in x:
                  for obj in y:
                      if obj.get_type() == 'Candy':
                         return True
          return False

      def gametick(self):
          for x in self.map:
              for y in x:
                  for obj in y:
                      if obj.get_status():
                         obj.logic(self)
                      else:
                         del (obj)

          for x in self.map:
              for y in x:
                  for obj in y:
                      obj.draw()
                     
     
      def process_events(events, packman):
           for event in events:
                 if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        sys.exit(0)
                 elif event.type == KEYDOWN:
                        if event.key == K_LEFT:            
                                packman.direction = 3
                        elif event.key == K_RIGHT:
                                packman.direction = 1
                        elif event.key == K_UP:
                                packman.direction = 4
                        elif event.key == K_DOWN:
                                packman.direction = 2
                        elif event.key == K_SPACE:
                                packman.direction = 0

      def mainloop(self, screen, backgraund):
         while True:
                self.process_events(pygame.event.get())
                pygame.time.delay(100)
                self.gametick()
                draw_background(screen, background)
                ghost.draw(screen)
                pygame.display.update()

if __name__ == '__main__':
        init_window()
        tile_size = 32
        map_size = 16
        ghost = Ghost(5, 5, tile_size, map_size)
        background = pygame.image.load("./resources/background.png")
        screen = pygame.display.get_surface()
        game = Game(config)
        game.mainloop(screen, background)
            
