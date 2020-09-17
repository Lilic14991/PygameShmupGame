# Shmup game
# Pygame template - skeleton for a  new pygame project
import pygame
from pygame.sprite import Group
import random
import os

width = 800
height = 600
FPS = 30

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# podesiti assets folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png'))

class Player(pygame.sprite.Sprite):
    # Sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Surface za crtanje u pygame
        self.image = player_img.convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > width:
            self.rect.right = 0

# Inicijalizacija pygame i kreiranje screen-a
pygame.init()
# mixer f-ja je za zvuk u nasoj igrici
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
# Sprites => objekti na ekranu koji mogu da se pomeraju
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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


    all_sprites.update()
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
    # ========================================
    screen.fill(black)
    all_sprites.draw(screen)



    # *after* posle crtanja svih slika, flip the display
    pygame.display.flip()
    # Double Buffering

pygame.quit()


