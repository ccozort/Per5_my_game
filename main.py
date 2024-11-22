# this file was created by: Chris Cozort
# This game engine content was derived from Chris Bradfields content
# github test
# this is where we import libraries and modules
import pygame as pg
from settings import *
from utils import *
# from sprites import *
from sprites_side_scroller import *
# from sprites_top_and_side import *
from tilemap import *
from os import path
# we are editing this file after installing git
# git test
# git test



# currentLevel = "level" + str(currentLevel + 1) + ".txt"

'''
Elevator pitch: I want to create a game that follows an apprentice mage from the bottom of a tower to the top, leveling up as he climbs to the top to defeat the evil wizard...

GOALS: to ascend the tower
RULES: jump, cast spells, shields attack, cannot move up until puzzles and enemies defeated 
FEEDBACK: Damage meter, spells interactions 
FREEDOM: x and y movement with jump, platforming

What's the sentence: Shoot iceblock with fireball melt iceblock to advance...

Alpha goal: to create a sidescroller setup gravity, platform collision, jump

'''

'''
Sources:
https://www.pygame.org/docs/ref/mouse.html - used to see if mouse is clicked

Prompt for ChatGPT:


'''

def draw_stat_bar(surf, x, y, w, h, pct, fill_color, outline_color):
    if pct < 0:
        pct = 0
    BAR_LENGTH = w
    BAR_HEIGHT = h
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLACK, outline_rect)
    pg.draw.rect(surf, fill_color, fill_rect)
    pg.draw.rect(surf, outline_color, outline_rect, 2)


# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    # sound mixer...
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chris' Coolest Game Ever...")
    self.playing = True
    self.running = True
    self.score = 0
    self.highscore = 0
    self.key_pressed = False
    self.key_start = 0
    self.key_elapsed = 0
    self.currentLevel = 1
    self.game_mode = "topdown"
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.img_folder = path.join(self.game_folder, 'images')
    self.snd_folder = path.join(self.game_folder, 'sounds')
    # self.player_img = pg.image.load(path.join(self.img_folder, 'bell.png'))
    # load images
    self.ladder_img = pg.image.load(path.join(self.img_folder, 'ladder.png'))
    self.dk_img = pg.image.load(path.join(self.img_folder, 'DK.png'))

    # load sounds
    self.jump_snd = pg.mixer.Sound(path.join(self.snd_folder, 'jump_07.wav'))
    pg.mixer.music.load(path.join(self.snd_folder, 'background_music.mp3'))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(loops=-1)

    self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + ".txt"))
  def load_next_level(self):
    # kill all sprites to free up memory
    self.currentLevel += 1
    for s in self.all_sprites:
       s.kill()
      #  print(len(self.all_sprites))
    # From load data to create new map object with level parameter
    self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + ".txt"))
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        # print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        if tile == 'U':
          Powerup(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
        if tile == 'T':
          Portal(self, col, row)
        if tile == 'R':
          Projectile(self, col, row)
        if tile == 'V':
          Moving_Platform(self, col, row)
        if tile == 'L':
          Ladder(self, col, row)
        if tile == 'A':
          Lava(self, col, row)
        if tile == 'B':
          Barrel(self, col, row)
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'D':
          self.dk = DK(self, col, row)

  def new(self):
    self.load_data()
    # create game countdown timer
    self.game_timer = Timer(self)
    # set countdown amount
    self.game_timer.cd = 45
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_platforms = pg.sprite.Group()
    self.all_portals = pg.sprite.Group()
    self.all_barrels = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group()
    self.all_projectiles = pg.sprite.Group()
    self.all_explosions = pg.sprite.Group()
    self.all_ladders = pg.sprite.Group()
    self.all_lava = pg.sprite.Group()
    # instantiating the class to create the player object 
    # self.player = Player(self, 5, 5)
    # self.mob = Mob(self, 100, 100)
    # self.wall = Wall(self, WIDTH//2, HEIGHT//2)
    # # instantiates wall and mob objects
    # for i in range(12):
    #   Wall(self, TILESIZE*i, HEIGHT/2)
    #   Mob(self, TILESIZE*i, TILESIZE*i)
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        # print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        if tile == 'U':
          Powerup(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
        if tile == 'T':
          Portal(self, col, row)
        if tile == 'R':
          Projectile(self, col, row)
        if tile == 'V':
          Moving_Platform(self, col, row)
        if tile == 'L':
          Ladder(self, col, row)
        if tile == 'A':
          Lava(self, col, row)
        if tile == 'B':
          Barrel(self, col, row)
    
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'D':
          self.player = DK(self, col, row)
    for i in range(10):
      p = Powerup(self, randint(0, WIDTH//TILESIZE), randint(0, HEIGHT//TILESIZE))
      print(p.rect.x)
         

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
          if self.playing:
            self.playing = False
          self.running = False
        
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_SPACE:
            if not self.key_pressed:
              self.player.jump()
              self.key_start = pg.time.get_ticks()
              self.key_pressed = True
        
        if event.type == pg.KEYUP:
          if event.key == pg.K_s:
            self.key_pressed = False
            if self.key_elapsed < 300:
              self.player.vel.y += GRAVITY
            
            print("Spacebar held for", self.key_elapsed, "milliseconds")
        
        

        

  # process
  # this is where the game updates the game state
  def update(self):

    self.game_timer.ticking()
    self.key_elapsed = pg.time.get_ticks() - self.key_start
    if self.key_elapsed > 300:
      print("max jump factor reached...")
    # if self.player.health < 95:
    #   self.playing = False
    # if self.game_timer.cd < 40:
    #   for s in self.all_sprites:
    #     s.kill()
    #   self.load_level("level2.txt")
    # update all the sprites...and I MEAN ALL OF THEM
    # for w in self.all_walls:
    #   if self.player.pos.x > WIDTH - WIDTH/3:
    #     w.rect.x -= self.player.vel.x
    self.all_sprites.update()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  # output
  def draw(self):
    self.screen.fill(WHITE)
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, str(self.player.health), 24, BLACK, WIDTH/2, HEIGHT/2)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.game_timer.get_countdown()), 24, WHITE, WIDTH/30, HEIGHT/16)
    self.draw_text(self.screen, str(self.player.coins), 24, WHITE, WIDTH-100, 50)
    draw_stat_bar(self.screen, self.player.rect.x, self.player.rect.y-TILESIZE, TILESIZE, 25, self.player.health, RED, WHITE)
    pg.display.flip()

  def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        # pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        # pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(self.screen, "NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            # with open(path.join(self.dir, HS_FILE), 'w') as f:
            #     f.write(str(self.score))
        else:
            self.draw_text(self.screen, "High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()


  def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False



if __name__ == "__main__":
  # instantiate
  g = Game()
  g.show_go_screen()
  while g.playing:
    g.new()
    g.run()
  