# Pygame template - skeleton for a  new pygame project
import pygame
import random

width = 360
height = 480
FPS = 30

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# Inicijalizacija pygame i kreiranje screen-a
pygame.init()
# mixer f-ja je za zvuk u nasoj igrici
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
# Sprites => objekti na ekranu koji mogu da se pomeraju
all_sprites = pygame.sprite.Group()

# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)
    '''
    Process input (Events)
    '''
    for event in pygame.event.get():
        # provera za zatvaranje prozora
        if event.type == pygame.QUIT:
            running = False


    # Update
    all_sprites.Update()
    # Draw / render
    # =====================================
    # Primary Colors:
    # $ Red,Green,Blue
    # Secondary Colors:
    # $ red + green = yellow
    # $ green + blue = cyan
    # $ blue + red = magenta
    # All Colors:
    # $ red + green + blue = white
    # $ no color = black
     
    #  RGB Colors
    #  0, 255
    #=========================================

    screen.fill(black)
    all_sprites.draw(screen)

    # *after* posle crtanja svih slike, flip the display
    pygame.display.flip()
    # Double Buffering

pygame.quit()


