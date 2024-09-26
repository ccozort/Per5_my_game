# this file was created by: Chris Cozort

# this is where we import libraries and modules
import pygame as pg
from settings import *
from sprites import *

# create a game class that carries all the properties of the game and methods
class Game:
  def init(self):
    pass
  def __init__(self):
    pg.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chris' Coolest Game Ever...")
    self.playing = True
  # this is where the game creates the stuff you see and hear
  def new(self):
    # create sprite group using the pg library
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    # instantiating the class to create the player object 
    self.player = Player(self, 50, 50)
    self.mob = Mob(self, 100, 100)
    self.wall = Wall(self, WIDTH//2, HEIGHT//2)

    for i in range(6):
      w = Wall(self, TILESIZE*i, TILESIZE*i)
      print(w.rect.x)

# this is a method
# methods are like functions that are part of a class
# the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()

    pg.quit()
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites...and I MEAN ALL OF THEM
    self.all_sprites.update()

 

  # output
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.all_sprites.draw(self.screen)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate 
  g = Game()
  g.new()
  g.run()