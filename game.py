#!/usr/bin/python
import pygame, sys
from random import randint


class Player(pygame.sprite.Sprite):

    __speed_x = 50
    __speed_y = 10
    __health = 3
    __is_jumping = False
    __is_climbing = False

    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.image.fill([255, 0, 0])

    def action(self, event, latters_list):
        self.__move(event, latters_list)

    def __move(self, event, latters_list):
        if not self.__is_climbing:  # no allow horizontal movement if climbing
            self.__move_x(event)
        self.__jump(event, latters_list)

    def __move_x(self, event):
        if event.key == pygame.K_LEFT:
            if self.rect.x > 0:
                self.rect.x -= self.__speed_x
            else:
                self.rect.x = 0
        if event.key == pygame.K_RIGHT:
            if self.rect.x < WIN_WIDTH - self.rect.width:
                self.rect.x += self.__speed_x
            else:
                self.rect.x = WIN_WIDTH - self.rect.width

    def __move_y(self, event):
        if event.key == pygame.K_DOWN:
            if self.rect.y < WIN_HEIGHT - self.rect.height:
                self.rect.y += self.__speed_y
            else:
                self.rect.y = WIN_WIDTH - self.rect.height

    def __jump(self, event, latters_list):
        if not self.__is_jumping:
            if event.key == pygame.K_SPACE:
                self.__climb(latters_list)
                if self.rect.y > 0:
                    self.rect.y -= self.__speed_y * 3
                else:
                    self.rect.y -= 0

    def __climb(self, latters_list):
        hit_list = pygame.sprite.spritecollide(self, latters_list, False)
        if hit_list:
            print "climbing"
            self.__is_climbing = True
            self.rect.y += 1

    def gravity(self):
        ''' Force player to ground if not jumping '''
        if not self.__is_jumping and not self.__is_climbing:
            #self.rect.y += self.__speed_y / 4
            self.rect.y += 1

    def check_collisions(self, platforms, barrels):
        ''' Will check for Player for collisions '''
        # check for collision with platforms
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hit_list:
            if self.rect.y < hit.rect.y:    # player hits top of platform
                self.rect.bottom = hit.rect.top
            elif self.rect.y > hit.rect.y:  # player hits bottom of platform
                if self.__is_climbing:    # player is climbing latter so place at top instead
                    self.rect.bottom = hit.rect.top
                    self.__is_climbing = False
                else:
                    self.rect.top = hit.rect.bottom # TODO: hiting side moves player to top or bottom
            else:
                self.rect.bottom = hit.rect.top
        # check if barrel has hit player
        hit_list = pygame.sprite.spritecollide(self, barrels, True)
        if hit_list:    # player has been hit by barrel
            self.__health -= 1
            if self.__health <= 0: self.kill()  # destroy player if __health == 0 GAMEOVER

class Platform(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, width, height):
        pygame.sprite.Sprite.__init__(self)
        # create plateform surface
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()   # get rect info
        self.image.fill([237, 8, 104])    # red plateform
        self.rect.x = x_pos
        self.rect.y = y_pos

class Barrel(pygame.sprite.Sprite):

    speed_x = 1
    speed_y = 1
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        # create brown barrel at specified position
        self.image = pygame.Surface([30, 18])
        self.image.fill([160,82,45])
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

        #self.speed_x = randint(3, 5)

    def bounce(self, force, platforms):
        # check if hits floor
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        if hit_list:
            hit = hit_list[0]   # hit platform
            # used to prevent dragging of barrels against platform
            if self.rect.y > hit.rect.y: # top of barrel hits platform
                self.rect.top = hit.rect.bottom
            else:   # bottom of barrel hits platform
                self.rect.bottom = hit.rect.top
            self.speed_y = -self.speed_y

    def move(self):
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y

    def spawn(self, row):
        self.rect.x = WIN_WIDTH / 1.25
        self.rect.y = WIN_HEIGHT / (row + 1)

    def destroy(self):
        if self.rect.x < WIN_WIDTH / 5:
            self.kill()

class Latter(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill([75, 181, 188])
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos


''' Platform Utility Routine '''
def create_platforms(sprite_list):
    platforms_list = pygame.sprite.Group()

    p_width, p_height = 1000, 50
    p_centerx = WIN_WIDTH / 2 - p_width / 2
    p_centery = WIN_HEIGHT / 2 - p_height / 2

    platform = Platform(p_centerx, WIN_HEIGHT - WIN_HEIGHT / 4, p_width, p_height)
    platforms_list.add(platform)
    sprite_list.add(platform)

    platform = Platform(p_centerx, WIN_HEIGHT - WIN_HEIGHT / 2.20, p_width, p_height)
    platforms_list.add(platform)
    sprite_list.add(platform)

    platform = Platform(p_centerx, WIN_HEIGHT - WIN_HEIGHT / 1.5, p_width, p_height)
    platforms_list.add(platform)
    sprite_list.add(platform)

    # creates platform DK stands on
    platform = Platform(WIN_WIDTH / 4, WIN_HEIGHT / 4, p_width / 4, p_height / 1.5)
    platforms_list.add(platform)
    sprite_list.add(platform)

    return platforms_list

''' Barrel Utility Routines '''
def create_barrels(barrels_list, sprite_list):

    barrel = Barrel(WIN_WIDTH / 3, WIN_HEIGHT / 2)
    barrel.spawn(1.5)
    barrels_list.add(barrel)
    sprite_list.add(barrel)

    barrel = Barrel(WIN_WIDTH / 5, WIN_HEIGHT / 2)
    barrel.spawn(0.5)
    barrels_list.add(barrel)
    sprite_list.add(barrel)

    barrel = Barrel(WIN_WIDTH / 4, WIN_HEIGHT / 2)
    barrel.spawn(3)
    barrels_list.add(barrel)
    sprite_list.add(barrel)
def move_barrels(barrels_list):
    ''' have barrels roll '''
    for barrel in barrels_list:
        barrel.move()
def bounce_barrels(barrels_list, platforms_list):
    ''' Bounce barrels if it collides with platforms '''
    for barrel in barrels_list:
        barrel.bounce(10, platforms_list)
def update_barrels(barrels_list, platforms_list):
    move_barrels(barrels_list)
    bounce_barrels(barrels_list, platforms_list)
    destroy_barrels(barrels_list)
def destroy_barrels(barrels_list):
    ''' destroys barrels after it crosses a certain point '''
    for barrel in barrels_list:
        barrel.destroy()

''' Latter Utility Routine '''
def create_latters(background_sprites):
    latters_list = pygame.sprite.Group()
    latter = Latter(WIN_WIDTH / 1.5, WIN_HEIGHT / 1.75, 50, 195)
    latters_list.add(latter)
    background_sprites.add(latter)

    latter = Latter(WIN_WIDTH / 4, WIN_HEIGHT / 2.8, 50, 205)
    latters_list.add(latter)
    background_sprites.add(latter)

    return latters_list

pygame.init()
# game configuration
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
SCREEN_SIZE = WIN_WIDTH, WIN_HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()
FPS = 60

# player creation
player = Player(WIN_WIDTH / 2, WIN_HEIGHT/1.4)
front_sprites = pygame.sprite.Group()
front_sprites.add(player)

# maintains list of sprites to be drawn
all_sprites = pygame.sprite.Group()

# create platforms
background_sprites = pygame.sprite.Group()
platforms_list = create_platforms(background_sprites)

# barrel initialization
middle_sprites = pygame.sprite.Group()
barrels_list = pygame.sprite.Group()
barrel_timer = 0
create_barrels(barrels_list, middle_sprites)

# create latters
latters_list = create_latters(background_sprites)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.KEYDOWN:  # check for player movement
            if event.key == pygame.K_ESCAPE: sys.exit(0)  # quit game

            player.action(event, latters_list)

    barrel_timer += 1
    if barrel_timer % 200 == 0:
        create_barrels(barrels_list, front_sprites)

    update_barrels(barrels_list, platforms_list)

    player.gravity()
    player.check_collisions(platforms_list, barrels_list)

    screen.fill([30, 3, 8])      # erase all content
    background_sprites.draw(screen)    # draw all sprites on screen
    front_sprites.draw(screen)
    pygame.display.flip()       # update display
    clock.tick(FPS)              # FPS

pygame.quit()
