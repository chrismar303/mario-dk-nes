import pygame
pygame.init()

# confiugre window
WIN_WIDTH = 500
WIN_HEIGHT = 320
WIN_SIZE = WIN_WIDTH, WIN_WIDTH

pygame.display.set_caption("Donkey Kong Vs Mario")
pygame.display.set_mode(WIN_SIZE)

is_playing = True
while is_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_playing = False



pygame.quit()
