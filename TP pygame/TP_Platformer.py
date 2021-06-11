import pygame, random, sys, time
from pygame.locals import *


# Usado https://kenney.nl/assets/jumper-pack    
#       https://kenney.nl/assets/platformer-characters


HEIGHT = 960
WIDTH = 640
GRID_SIZE = 64

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()

# Inicializacion
fps = 60
framePerSec = pygame.time.Clock() 
ACC = 0.5       #que tan rapido se mueve el personaje
FRIC = -0.12

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
display_surface.fill(BLACK)
pygame.display.set_caption("TP Desarrollo de Juegos - Platformer")


# Carga de raw assets
bg1 = pygame.image.load("img/PNG/Background/bg_layer1.png")
bg2 = pygame.image.load("img/PNG/Background/bg_layer2.png")
bg3 = pygame.image.load("img/PNG/Background/bg_layer3.png")
platform = pygame.image.load("img/PNG/Environment/ground_grass.png")
spikes = pygame.image.load("img/PNG/Environment/spikes_top.png")
player_image_big = pygame.image.load("img\Player\PNG\Player\Poses\player_idle.png")
player_image_big_jump = pygame.image.load("img\Player\PNG\Player\Poses\player_jump.png")
star_1_big = pygame.image.load("img\PNG\Items\gold_1.png")
star_2_big = pygame.image.load("img\PNG\Items\gold_2.png")
star_3_big = pygame.image.load("img\PNG\Items\gold_3.png")
star_4_big = pygame.image.load("img\PNG\Items\gold_4.png")

# Imagenes reducidas
player_image = pygame.transform.scale(player_image_big, (60, 70))
player_image_jump = pygame.transform.scale(player_image_big_jump, (60, 70))
platform_small = pygame.transform.scale(platform, (120, 48))
spikes_small = pygame.transform.scale(spikes, (50, 32))
star_1 = pygame.transform.scale(star_1_big, (42, 42))
star_2 = pygame.transform.scale(star_2_big, (33, 42))
star_3 = pygame.transform.scale(star_3_big, (25, 42))
star_4 = pygame.transform.scale(star_4_big, (7, 42))

myfont = pygame.font.SysFont("Verdana", 15)

class Player(pygame.sprite.Sprite):
    def __init__(self, player_image):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(60, 100))
        self.pos = pygame.math.Vector2((10, 900))
        self.vel = pygame.math.Vector2((0, 0))
        self.acc = pygame.math.Vector2((0, 0))
        self.current_level = 0
        self.score = 0

    def move(self):
        self.acc = pygame.math.Vector2((0, 0.5))
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT]:
            self.image = pygame.transform.flip(self.image, True, False)
            self.acc.x = -ACC
        if teclas[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH - 20
        if self.pos.x < 0:
            self.pos.x = 0 + 20                 #cuento 20 porque el player es de 40 px
        if self.pos.y > HEIGHT:
            self.pos.x = 10
            self.pos.y = 900
            self.score = 0
            stars.add(star)
            stars1.add(star1)
            sprites.add(stars)
            sprites.add(stars1)
            sprites2.add(star)
            sprites2.add(stars1)
        if self.pos.y < 0:                      #paso de nivel
            self.current_level += 1
            stars.add(star)                     #agrego los sprites de las estrellas al pasar de nivel
            stars1.add(star1)
            sprites2.add(stars)
            sprites2.add(stars1)
            cambioNivel(bg1, bg3, sprites2, plataformas2, plataformas_spike2, self.score)       #cambio de nivel con un nuevo background, sprite, plataformas y con el score que se tenia

        self.rect.midbottom = self.pos

    def jump(self, plataformas):
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        if hits:                                # Para evitar mas de un salto
            self.vel.y = -15
            self.image = player_image_jump


    def update(self, plataformas, plataformas_spike, score):
        self.score = score
        
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        if self.vel.y > 0:
            if hits:
                self.image = player_image       #actualizo la imagen cuando "aterriza" para que no quede siempre saltando
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1

        hits_spiked = pygame.sprite.spritecollide(self, plataformas_spike, False)
        if hits_spiked:
            stars.add(star)                     #cargo las estrellas porque se "perdio" y se vuelve a empezar
            stars1.add(star1)
            sprites.add(stars)
            sprites.add(stars1)
            sprites2.add(stars)
            sprites2.add(stars1)
            self.pos.x = 10
            self.pos.y = 900
            self.score = 0

        hits_stars = pygame.sprite.spritecollide(self, stars, True)             #True no incrementa el score constantemente pero remueve el sprite.
        hits_stars1 = pygame.sprite.spritecollide(self, stars1, True)
        if hits_stars:
            self.score = 10 + score
        if hits_stars1:
            self.score = 10 + score


class Star(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.is_animating = False
        self.sprites = []
        self.sprites.append(star_1)
        self.sprites.append(star_2)
        self.sprites.append(star_3)
        self.sprites.append(star_4)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [posx, posy]

    def update(self):
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def move(self):
        pass

class PlataformaPiso(pygame.sprite.Sprite):
    def __init__(self, platform):
        super().__init__()
        self.image = platform
        #self.surf = pygame.Surface((380, 94))
        self.rect = self.image.get_rect(center = ((380 / 2) - 50, HEIGHT))

    def move(self):
        pass

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, platform_small, block):
        super().__init__()
        self.image = platform_small
        self.rect = self.image.get_rect(center = block)

    def move(self):
        pass

class PlataformaSpike(pygame.sprite.Sprite):
    def __init__(self, spikes_small, block):
        super().__init__()
        self.image = spikes_small
        self.rect = self.image.get_rect(center = block)

    def move(self):
        pass
        
def cambioNivel(bg1, bg2, sprites, plataforma, plataforma_spiked, score):
    if player.current_level > 1:
        print("El juego solo tiene 2 niveles. Termina")
        print("El score del jugador fue: ",player.score)
        pygame.quit()
    player.pos = pygame.math.Vector2((10, 900))
    inGame = True
    while inGame:

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                #inGame = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inGame = False
                if event.key == pygame.K_UP:
                    player.jump(plataforma)
                    
        for sprite in sprites:              #sin este for la imagen al saltar se repite constantemente
            display_surface.blit(sprite.image, sprite.rect)
            sprite.move()
        
        display_surface.blit(bg1, (0, 0))
        display_surface.blit(bg2, (0, -600))
        star.update()
        star1.update()
        
        player.update(plataforma, plataforma_spiked, player.score)

        for sprite in sprites:
            display_surface.blit(sprite.image, sprite.rect)
            sprite.move()

        text = myfont.render("Score {0}".format(player.score), 1, (0,0,0))
        display_surface.blit(text, (15,20))
    
        pygame.display.update()

        framePerSec.tick(fps)


#Jugador
player = Player(player_image)

#Estrellas
stars = pygame.sprite.Group()
stars1 = pygame.sprite.Group()

star = Star(4 * GRID_SIZE, 9 * GRID_SIZE)
star1 = Star(2 * GRID_SIZE, GRID_SIZE - 15)

stars.add(star)
stars1.add(star1)

# Plataformas del primer nivel
plat = [(7 * GRID_SIZE, 11 * GRID_SIZE), (3 * GRID_SIZE, 8 * GRID_SIZE), (7 * GRID_SIZE, 5 * GRID_SIZE), (2 * GRID_SIZE, 2 * GRID_SIZE)]

plataformas = pygame.sprite.Group()

for block in plat:
    plataformas.add(Plataforma(platform_small, block))

piso = PlataformaPiso(platform)
plataformas.add(piso)

plat_spiked = (7 * GRID_SIZE, 11 * GRID_SIZE - 42)
plataformas_spike = pygame.sprite.Group()
platform_spiked = PlataformaSpike(spikes_small, plat_spiked) #42 por el alto de la plataforma small
plataformas_spike.add(platform_spiked)


# Plataformas del segundo nivel
plat2 = [(5 * GRID_SIZE, 11 * GRID_SIZE), (7 * GRID_SIZE, 8 * GRID_SIZE), (3 * GRID_SIZE, 5 * GRID_SIZE), (7 * GRID_SIZE, 2 * GRID_SIZE)]
plataformas2 = pygame.sprite.Group()

for block2 in plat2:
    plataformas2.add(Plataforma(platform_small, block2))

plat_spiked2 = (7 * GRID_SIZE, 8 * GRID_SIZE - 42)
plataformas_spike2 = pygame.sprite.Group()
plataformas2.add(piso)
platform_spiked2 = PlataformaSpike(spikes_small, plat_spiked2) #42 por el alto de la plataforma small
plataformas_spike2.add(platform_spiked2)

#Sprites 1er nivel
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(plataformas)
sprites.add(plataformas_spike)
sprites.add(stars)
sprites.add(stars1)

#Sprites 2do nivel
sprites2 = pygame.sprite.Group()
sprites2.add(player)
sprites2.add(plataformas2)
sprites2.add(plataformas_spike2)
sprites2.add(stars)
sprites2.add(stars1)


cambioNivel(bg1, bg2, sprites, plataformas, plataformas_spike, 0)       #comienza el programa. el 0 es el score inicial.