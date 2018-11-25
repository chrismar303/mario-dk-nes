#!/usr/bin/python
import pygame, sys

pygame.init()

class Player(pygame.sprite.Sprite):

    move_x = 20
    move_y = 20
    health = 3

    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.image.fill((255, 255, 255))

    def move(self, event):
        self.__move_x(event)
        self.__move_y(event)

    def __move_x(self, event):
        if event.key == pygame.K_LEFT:
            if self.rect.x > 0:
                self.rect.x -= self.move_x
            else:
                self.rect.x = 0
        if event.key == pygame.K_RIGHT:
            if self.rect.x < WIN_WIDTH - self.rect.width:
                self.rect.x += self.move_x
            else:
                self.rect.x = WIN_WIDTH - self.rect.width

    def __move_y(self, event):
        if event.key == pygame.K_UP:
            if self.rect.y > 0:
                self.rect.y -= self.move_y
            else:
                self.rect.y -= 0
        if event.key == pygame.K_DOWN:
            if self.rect.y < WIN_HEIGHT - self.rect.height:
                self.rect.y += self.move_y
            else:
                self.rect.y = WIN_WIDTH - self.rect.height

    def jump(self):
        pass

    def check_collisions(self, platforms, barrels):
        # check for collision with platforms
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hit_list:
            if self.rect.y < hit.rect.y:    # player hits top of platform
                self.rect.bottom = hit.rect.top
            elif self.rect.y > hit.rect.y:  # player hits bottom of platform
                self.rect.top = hit.rect.bottom # TODO: hiting side moves player to top or bottom
            else:
                self.rect.bottom = hit.rect.top
        # check if barrel has hit player
        hit_list = pygame.sprite.spritecollide(self, barrels, True)
        print self.health
        if hit_list:
            self.health -= 1
            if self.health <= 0: self.kill()  # destroy player if health == 0 GAMEOVER

class Platform(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, width, height):
        pygame.sprite.Sprite.__init__(self)
        # create plateform surface
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()   # get rect info
        self.image.fill([255, 0, 0])    # red plateform
        self.rect.x = x_pos
        self.rect.y = y_pos

class Barrel(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        # create brown barrel at specified position
        self.image = pygame.Surface([30, 18])
        self.image.fill([160,82,45])
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

def create_platforms(platforms_list, all_sprites):
    p_width, p_height = 1000, 50
    p_centerx = WIN_WIDTH / 2 - p_width / 2
    p_centery = WIN_HEIGHT / 2 - p_height / 2

    platform = Platform(p_centerx, WIN_HEIGHT - WIN_HEIGHT / 4, p_width, p_height)
    platforms_list.add(platform)
    all_sprites.add(platform)

    platform = Platform(p_centerx, WIN_HEIGHT - WIN_HEIGHT / 2.20, p_width, p_height)
    platforms_list.add(platform)
    all_sprites.add(platform)

    platform = Platform(p_centerx, WIN_HEIGHT - WIN_HEIGHT / 1.5, p_width, p_height)
    platforms_list.add(platform)
    all_sprites.add(platform)

    # creates platform DK stands on
    platform = Platform(WIN_WIDTH / 4, WIN_HEIGHT / 4, p_width / 4, p_height / 1.5)
    platforms_list.add(platform)
    all_sprites.add(platform)

# game configuration
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
SCREEN_SIZE = WIN_WIDTH, WIN_HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()
FPS = 60
# maintains list of sprites to be drawn
all_sprites = pygame.sprite.Group()

# create platforms
platforms_list = pygame.sprite.Group()
create_platforms(platforms_list, all_sprites)

# player creation
player = Player(WIN_WIDTH / 2, WIN_HEIGHT / 2)
all_sprites.add(player)

# barrel initialization
barrels_list = pygame.sprite.Group()
barrel = Barrel(WIN_WIDTH / 3, WIN_HEIGHT / 2)
barrels_list.add(barrel)
all_sprites.add(barrel)

# barrel initialization
barrel = Barrel(WIN_WIDTH / 5, WIN_HEIGHT / 2)
barrels_list.add(barrel)
all_sprites.add(barrel)

# barrel initialization
barrel = Barrel(WIN_WIDTH / 4, WIN_HEIGHT / 2)
barrels_list.add(barrel)
all_sprites.add(barrel)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.KEYDOWN:  # check for player movement
            player.move(event)  # handle user movement
            if event.key == pygame.K_ESCAPE: sys.exit(0)  # quit game



    player.check_collisions(platforms_list, barrels_list)

    screen.fill((0, 0, 0))      # erase all content
    all_sprites.draw(screen)    # draw all sprites on screen
    pygame.display.flip()       # update display
    clock.tick(FPS)              # FPS

pygame.quit()
