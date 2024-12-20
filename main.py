# this file was created by: Chris Cozort
# This game engine content was derived from Chris Bradfields content
# github test
# this is where we import libraries and modules
import pygame as pg
from settings import *
from utils import *
# from sprites import *
from sprites_vert_scroller import *
# from sprites_side_scroller import *
# from sprites_top_and_side import *
from tilemap import *
from os import path
import random
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
    self.key_pressed = False
    self.key_start = 0
    self.key_elapsed = 0
    self.currentLevel = 0
    self.game_mode = "topdown"
    self.time_to_complete = 0
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    x = round((47/23), 2)
    print(float(x))
    print("data has been loaded")
    try:
      self.game_folder = path.dirname(__file__)
      print("successfully setup game folder...")
    except:
       print("unable to setup game folder...")
    self.check_highscore()
    self.img_folder = path.join(self.game_folder, 'images')
    self.snd_folder = path.join(self.game_folder, 'sounds')
    # self.player_img = pg.image.load(path.join(self.img_folder, 'bell.png'))
    # load images
    self.ladder_img = pg.image.load(path.join(self.img_folder, 'ladder.png'))
    self.dk_img = pg.image.load(path.join(self.img_folder, 'DK.png'))
    # load sounds
    self.jump_snd = pg.mixer.Sound(path.join(self.snd_folder, 'jump_07.wav'))
    # pg.mixer.music.load(path.join(self.snd_folder, 'background_music.mp3'))
    # pg.mixer.music.set_volume(0.4)
    # pg.mixer.music.play(loops=-1)

    self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + ".txt"))
  def load_next_level(self):
    # kill all sprites to free up memory
    # self.currentLevel += 1
    for s in self.all_sprites:
       s.kill()
      #  print(len(self.all_sprites))
    # From load data to create new map object with level parameter
    # self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + ".txt"))
    self.map = Map(path.join(self.game_folder, "level1.txt"))
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
        if tile == 'p':
          Platform(self, col, row, 100, 20)
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'D':
          self.dk = DK(self, col, row)
  def check_highscore(self):
      # if the file exists
        if path.exists(HS_FILE):
          print("this exists...")
          with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                self.best_time = int(f.read())
        else:
          with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                self.best_time =  1000000
                f.write(str(100000))
        print("File created and written successfully.")
  def new(self):
    self.load_data()
    self.test_rect = pg.Rect(WIDTH/2, HEIGHT/2, 100, 50)
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
        if tile == 'p':
          Platform(self, col, row, 100, TILESIZE)
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'D':
          self.player = DK(self, col, row)
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
    keys = pg.key.get_pressed()
    if keys[pg.K_r] and keys[pg.K_ESCAPE]:
    # if keys[pg.K_r] and keys[pg.K_ESCAPE]:
        print("control")
        if self.playing:
            self.playing = False
        self.running = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
          print(self.game_timer.current_time)
          if self.game_timer.current_time < self.best_time:
            print("i got a best time")
            print(self.game_timer.current_time)
            print(self.best_time)
            self.best_time = self.game_timer.current_time
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
              f.write(str(self.game_timer.current_time))
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
  def update(self):
    if self.player.rect.y > HEIGHT + TILESIZE:
       self.load_next_level()
       print("i have fallen!")
    self.game_timer.ticking()
    self.key_elapsed = pg.time.get_ticks() - self.key_start
    if self.key_elapsed > 300:
      pass
      # print("max jump factor reached...")
    self.all_sprites.update()
    while len(self.all_platforms) < 15:
      width = random.randrange(50, 100)
      p = Platform(self, random.randrange(0, WIDTH//TILESIZE - width//TILESIZE), random.randrange(-5, 0), width, TILESIZE)
      if random.randint(0,9) > 4:
        c = Coin(self, p.rect.x//TILESIZE, p.rect.y//TILESIZE - 1)
        self.all_coins.add(c)
        self.all_sprites.add(c)
      self.all_platforms.add(p)
      self.all_sprites.add(p)
      
    if self.player.rect.top <= HEIGHT/4:
      print(str(len(self.all_platforms)))
      self.player.pos.y += abs(self.player.vel.y)
      for plat in self.all_platforms:
        plat.rect.y += abs(self.player.vel.y)
        if plat.rect.y >= HEIGHT:
          
          plat.kill()
          print(str(len(self.all_coins)))
      for coin in self.all_coins:
        coin.rect.y += abs(self.player.vel.y)
        if coin.rect.y >= HEIGHT:
          coin.kill()
          print(str(len(self.all_coins)))
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
    self.draw_text(self.screen, str(self.game_timer.current_time), 24, BLACK, WIDTH/30, HEIGHT/16)
    self.draw_text(self.screen, str(self.score), 24, BLACK, WIDTH-100, 50)
    self.draw_text(self.screen, "Best time is " + str(self.best_time), 24, BLACK, WIDTH-100, 100)
    draw_stat_bar(self.screen, self.player.rect.x, self.player.rect.y-TILESIZE, TILESIZE, 25, self.player.health, RED, WHITE)
    self.test_rect = pg.Rect(WIDTH/2, HEIGHT/2, 100, 50)
    pg.draw.rect(self.screen, RED, self.test_rect)
    pg.display.flip()
  def show_start_screen(self):
        self.load_data()
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Welcome to the game! ", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Best time: " + str(self.best_time), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
  def show_end_screen(self):
        print("File created and written successfully.")
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "You're done! ", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Best time: " + str(self.best_time), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
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
  # g.show_start_screen()
  while g.playing:
    g.new()
    g.run()
  g.show_end_screen()