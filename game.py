#!/usr/bin/python
import pygame, sys

pygame.init()

class Player(pygame.sprite.Sprite):

    move_x = 10
    move_y = 10

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
                self.rect.x = WIN_WIDTH -self.rect.width

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


SCREEN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 720

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group() # maintains list of sprites to be drawn
player = Player(100, 100)
all_sprites.add(player)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:  # check for player movement
            player.move(event)

    screen.fill((0, 0, 0))      # erase all content
    all_sprites.draw(screen)    # draw all sprites on screen
    pygame.display.flip()       # update display
    clock.tick(60)

pygame.quit()
