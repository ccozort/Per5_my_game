# This file was created by: Chris Cozort

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from os import path
from utils import *

vec = pg.math.Vector2

SPRITESHEET = 'sprite_sheet.png'

dir = path.dirname(__file__)
img_dir = path.join(dir, "images")

# sets up file with multiple images...
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, scale):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width*scale, height*scale))
        return image



class Player(Sprite):
    # this initializes the properties of the player class including the x y location, and the game parameter so that the the player can interact logically with
    # other elements in the game...
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((32, 32))
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.load_images()
        self.image = self.standing_image
        # self.image = self.game.player_img
        self.image.set_colorkey(BLACK)
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        self.jump_power = 35
        self.jumping = False
        self.climbing = False
        self.cd = Cooldown()
        self.invulnerable = Cooldown()
        self.mouse_pos = (0,0)
        self.health = 100
        self.coins = 0
    def load_images(self):
        self.standing_image = self.spritesheet.get_image(0,0,32,32, 1)
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            self.shoot()
        if keys[pg.K_w]:
            if self.climbing:
                self.vel.y -= 1
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()
        if pg.mouse.get_pressed()[0]:
            
            self.shoot()
    def shoot(self):
        self.cd.event_time = floor(pg.time.get_ticks()/1000)
        if self.cd.delta > .01:
            # print('trying to create projectile')
            self.mouse_pos = pg.mouse.get_pos()
            p = Projectile(self.game, self.rect.x, self.rect.y)
            if self.mouse_pos[0] > self.pos.x:
                p.speed = 10
            else:
                p.speed = -10
            
            # print(p.rect.x)
            # print(p.rect.y)

    def jump(self):
        # print("im trying to jump")
        
        print(self.vel.y)
        self.rect.y += 2
        whits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        phits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        self.rect.y -= 2
        if whits or phits and not self.jumping:
            self.game.jump_snd.play()
            self.jumping = True
            self.vel.y = -self.jump_power
            # print('still trying to jump...')
            
    def collide_with_plats(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                # if self.vel.y < 0:
                #     self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
                # print("Collided on x axis")
        #     else:
        #         print("not working...for hits")
        # # else:
        #     print("not working for dir check")
    def collide_with_ladders(self):
        self.rect.y -= 16
        hits = pg.sprite.spritecollide(self, self.game.all_ladders, False)
        self.rect.y += 16
        if hits:
            self.climbing = True
        else:
            self.climbing = False
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                for m in self.game.all_mobs:
                    m.speed = 20
                    print(m.speed)
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
            if str(hits[0].__class__.__name__) == "Lava":
                self.health -= 1
                print(self.health)
                # self.invulnerable.event_time = floor(pg.time.get_ticks()/1000)
                # if self.invulnerable.delta > .01:
                #     self.health -= 1
            if str(hits[0].__class__.__name__) == "Portal":
                # self.game.load_level("level" + str(self.game.currentLevel + 1) ".txt")
                self.game.load_next_level()
            if str(hits[0].__class__.__name__) == "Mob":
                self.invulnerable.event_time = floor(pg.time.get_ticks()/1000)
                hits[0].image = self.game.hurtmob_image
                if self.invulnerable.delta > .01:
                    self.health -= 1
                if self.vel.y > 0:
                    print("collided with mob")
                    # hits[0].kill()
                else:
                    print("ouch I was hurt!!!")
            
    def update(self):
        self.cd.ticking()
        self.invulnerable.ticking()
        if not self.climbing:
            self.acc = vec(0, GRAVITY)
        else:
            self.acc = vec(0,0)
            self.acc.y += self.vel.y * FRICTION
            if abs(self.vel.y) < 0.5:
                self.vel.y = 0

        self.get_keys()
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.collide_with_plats('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_plats('y')

        self.collide_with_ladders()
        # teleport the player to the other side of the screen
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_ladders, False)
        self.collide_with_stuff(self.game.all_lava, False)
        self.collide_with_stuff(self.game.all_portals, False)
      

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            # self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

class Barrel(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_barrels
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.load_images()
        self.image = self.standing_image
        self.rect = self.image.get_rect()
        # self.radius = TILESIZE/2
        # pg.draw.circle(self.image, BROWN, self.rect.center, self.radius)
        self.image.set_colorkey(BLACK)
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 1
        print('barrel created')
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                    self.speed *= -1
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                    self.speed *= -1
                self.vel.x = 0
                self.rect.x = self.pos.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
    def load_images(self):
        self.standing_image = self.spritesheet.get_image(32,0,32,32, 1)
    def update(self):
        self.acc = vec(self.speed, GRAVITY)
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
    def update(self):
        self.rect.x += self.speed
        if self.rect.y < 0:
            self.kill()
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Lava(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_lava
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Moving_Platform(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def update(self):
        self.rect.x += 1
class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        print("created coin at", str(self.rect.x), str(self.rect.y))
class Portal(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_portals
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Ladder(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_ladders
        Sprite.__init__(self, self.groups)
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.load_images()
        self.image = self.standing_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.image.fill(YELLOW)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_image = self.spritesheet.get_image(64,0,32,32, 1)
class DK(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.dk_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.image.fill(YELLOW)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.groups = game.all_sprites, game.all_platforms
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        print("i have created a platform...")