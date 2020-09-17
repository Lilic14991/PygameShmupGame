# 1 - Import library
import pygame

from pygame.locals import *

# 2 - Initialize the game
pygame.init()

width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos=[100,100]
dest = (100,100)



# 3 - Load images
player = pygame.image.load("resources/images/ninja.png")
grass = pygame.image.load("resources/images/grass_template.jpg")
castle = pygame.image.load("resources/images/SMBCastle.png")

# 4 - keep looping through
while 1:
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements

    for x in range(width // grass.get_width() + 1):
        for y in range(height // grass.get_height() + 1):
            screen.blit(grass,dest), (x * 100, y * 100)
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    screen.blit(player, playerpos)
    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False

            # if it is quit the game

        # 9 - Move player
        if keys[0]:
            playerpos[1] -= 5
        elif keys[2]:
            playerpos[1] += 5
        if keys[1]:
            playerpos[0] -= 5
        elif keys[3]:
            playerpos[0] += 5

