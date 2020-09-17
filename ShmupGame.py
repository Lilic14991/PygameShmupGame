# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# Art from Kenny.nl
# Pygame template - skeleton for a  new pygame project
import pygame
from pygame.sprite import Group
import random
from os import path
# variabla img_dir je jednaka bilo gde se nalazi nasa img folder
# sa nasom grafikom za igru
img_dir = path.join(path.dirname(__file__), 'img')
# snd_dir gadja nasu lokacuju muzike za igru
snd_dir = path.join(path.dirname(__file__), 'snd')

width = 400
height = 600
FPS = 60
# 5000 mil sec
POWERUP_TIME = 5000

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)



# Inicijalizacija pygame i kreiranje screen-a
pygame.init()
# mixer f-ja je za zvuk u nasoj igrici
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
score = 0
# f-ja za crtanje
# font command pygame ce proci kroz PC i naci nesto najbilize
# nasem generickom imenu (times, arial...etc)
font_name = pygame.font.match_font('arial')
def draw_text(surf, text , size, x, y):
    font = pygame.font.Font(font_name, size)
    # py radi na principut pixel-a
    # tako da moramo nasu povrsinu da renderujemo
    # (Alias False, Anti-aliased True)
    # i boja u koju renderujemo
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# f-ja za stvaranje novih mobova
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
# f-ja za crtanje shield-a
def draw_shield_bar(surf,x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

def draw_lives(surf, x, y , life, img):
    for i in range(life):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# podesiti assets folder
#game_folder = os.path.dirname(__file__)
#img_folder = os.path.join(game_folder, "img")
#player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_blue.png'))

class Player(pygame.sprite.Sprite):
    # Sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Surface za crtanje u pygame
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.shield = 100
        # 250 milsec
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.life = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_SPACE] and not self.hidden:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > width:
           self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

        # if enough time has passed (1 second for now)
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 3000:
            self.hidden = False
            self.rectx = width / 2
            self.rect.bottom = height - 10

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    # player puca ()
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                # dodavanje zvuka za laser
                shoot_sound.play()
                # ako nam je power up da pucamo 2 metka
                # moramo da dodamo 2 metka  u nasu sprite
                # Gruop
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                # dodavanje zvuka za laser
                shoot_sound.play()


    def hide(self):
        # hide the player temporily
        # booleen fag za ne vidljivost player-a
        self.hidden = True
        # Privremeno sklanjamo player-a sa *screena* (bottom)
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, (height + 200))

# klasa za pravljenje Enemies
class Mob(pygame.sprite.Sprite):
    # Sprite za Mobove
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        # pravimo kopiju originalne slike mob-a
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # dodajemo radius za CBB
        self.radius = int(self.rect.width * .85 / 2)
        # da vidimo krug oko objekta (kao radius)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        # rect da se krece izmedju levog i desnog dela screen-a
        # (0, width - self.rect.width) ako ne napisemo 0 python
        # automatski pretpostavlja da je nula tu.
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        # get_ticks() koliko je proslo vremena od startovanja igre
        # svaki put kada rotirimamo obj azurirace se tick
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            # Rotacija rot | na nasu rotaciju dodajemo brzinu rotacije
            # i delimo je sa 360 (da ne bi dobili vrednost vecu od 360)  i da nam da sta je ostalo
            # (dobra praksa kao petlja)
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Ako objekat ode ispod dna ekrana, da se pojavi ponovo na vrhu
        # na random lokaciji
        if self.rect.top > height + 10 or self.rect.left <= -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(yellow)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill it if it moves off the top of the screen
        if self.rect.bottom < 0:
            # kill() - komanda uzima bilo koj sprite
            # i brise ga, uklanja ga iz bilo koje Gruop-e
            # ako se nalazi u nekoj
            self.kill()

class Powup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # type var nam daje random izbor za shield powup ili gun
        self.type = random.choice(['shield', 'gun'])
        # da nam vrati sliku koje je odabrana u rand izboru type-a
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves off the bottom of the screen
        if self.rect.top > height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self. image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, width / 2, height / 4)
    draw_text(screen, "A and D keys to  move, Space to fire", 22,
              width / 2, height / 2)
    draw_text(screen, "Press a key to begin", 18, width /2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False



# Load all game graphics | kada loadujemo grafiku po prvi put koristiti convert()
# =================================================================================
# load-ovanje background-a
background = pygame.image.load(path.join(img_dir, "space_1.png")).convert()
background_rect = background.get_rect()
# load-ovanje slike igraca
player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(black)
# load-ovanje slike mob-a
# meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
# dodavanje liste slika meteora
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorGrey_med2.png', 'meteorBrown_small1.png',
               'meteorBrown_big2.png', 'meteorGrey_big3.png', 'meteorGrey_small2.png',
               'meteorGrey_med2.png', 'meteorGrey_big3.png', 'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
# load-ovanje slike lasera
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
# ==================================================================================
# Dict za exploziju
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    explosion_anim['player'].append(img)
# Dict za slike power up-ova
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()


# load all game sounds
# zvuk lasera
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot1.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow_shield.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow_gun.wav'))
# lista za smestanje zvuka
expl_sounds = []
for snd in ['Explosion.wav', 'Explosion1.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)



# Sprites => objekti na ekranu koji mogu da se pomeraju
# Grupisi sve sprite-ove

# kada dodje do kraja sounda, pocinje iz pocetka (pygame)
pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        # Grupisati sve mobs(protivnike) radi lakseg odredjivanja
        # kada dodju obj(mob) u kontakt sa player-om
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        # spawn objekata

        player = Player()  # 1.a. igrac
        all_sprites.add(player)  # 1.b. dodavanje igraca u all_sprite grupu
        for i in range(8):
            newmob()
        score = 0


    # Keep loop running at the right speed
    clock.tick(FPS)
    '''
    Process input (events)
    '''
    for event in pygame.event.get():
        # provera za zatvaranje prozora
        if event.type == pygame.QUIT:
            running = False


    # Update
    all_sprites.update()

    # Check to see if a bullet hit a mob
    # gruopcollide() --> omogucava nam da spojimo dve grupe i da
    # proverimo da li se sudaraju
    # 1st True je za mobove koji budu pogodjeni da se obrisu
    # 2nd True je za bullets koji se sudare sa Mobovima da budu obrisani
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    # za svakog pogodjenog moba u listi hits stvara se novi mob
    # ako player unisti 3 mob-a stvorice se novih 3 etc...
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        # random.random() -> vraca decimal broj izmedju 0 i 1
        if random.random() > 0.9:
            powup = Powup(hit.rect.center)
            all_sprites.add(powup)
            powerups.add(powup)
        newmob()
    # Check to see if a mob hit a player
    # kada pokrenemo kod, ova komanda nam vraca listu (*hits*)
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.life -= 1
            player.shield = 100
    # check to see if player hit the powerups
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
            #pass


            # player.kill()
    # if the player died and the explosion has finished playing
    if player.life == 0 and not death_explosion.alive():
        # The alive() function just returns whether a particular sprite is alive.
        # Since we kill() the explosion when it finishes playing,
        # we can now end the game when it finishes.
        game_over = True


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
    #  blit() --> kopiraj px sa jedne stvari na drugu
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # crtanje text-a
    draw_text(screen, str(score), 18, width / 2, 10)
    # crtanje shield bar-a
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, width - 100, 5, player.life, player_mini_img)



    # *after* posle crtanja svih slika, flip the display
    pygame.display.flip()
    # Double Buffering

pygame.quit()


