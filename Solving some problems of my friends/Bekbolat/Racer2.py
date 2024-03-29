from math import pi
import pygame
import random
import time

pygame.init()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen
WIDTH = 400
HEIGHT = 590
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Background
BACKGROUND = pygame.image.load("Background.png")

# FPS
FPS = 60
timer = pygame.time.Clock()

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface(self.image.get_size())

        center = (WIDTH // 2, HEIGHT - self.image.get_height() // 2)
        self.rect = self.surf.get_rect(center=center)

        self.speed = 400
 
    def move(self):
        pixels_per_frame = self.speed // FPS
        pressed_keys = pygame.key.get_pressed()

        # if self.rect.top > 0:
        #     if pressed_keys[pygame.K_UP]:
        #         self.rect.move_ip(0, -pixels_per_frame)
        # if self.rect.bottom < HEIGHT:
        #     if pressed_keys[pygame.K_DOWN]:
        #         self.rect.move_ip(0, pixels_per_frame)
         
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-pixels_per_frame, 0)
        if self.rect.right < WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(pixels_per_frame, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)

#TEST start


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.width, self.height = self.image.get_size()
        self.surf = pygame.Surface(self.image.get_size())

        center = (random.randint(self.width // 2, WIDTH - self.width // 2), 
                  -self.height // 2)
        self.rect = self.surf.get_rect(center=center)

        self.speed = 400

    def move(self):
        global score
        pixels_per_frame = self.speed // FPS
        self.rect.move_ip(0, pixels_per_frame)
        if self.rect.top > HEIGHT:
            score += 1
            self.speed = random.randrange(400, 650, 50)
            center = (random.randint(self.width // 2, WIDTH - self.width // 2), 
                    -self.height // 2)
            self.rect.center = center

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("star1.png")
        self.image_rect = self.image.get_rect(bottomright=(40, 40))
        self.scale = pygame.transform.scale(self.image , (40, 40))
        self.surf = pygame.Surface((40, 40))
        
        center = (random.randint(40 // 2, WIDTH - 40 // 2), 
                  -40 // 2)
        self.rect = self.surf.get_rect(center=center)

        self.speed = 300  

    def move(self):
        global score
        pixels_per_frame = self.speed // FPS
        self.rect.move_ip(0, pixels_per_frame)
        if self.rect.top > HEIGHT:
            score += 1
            center = (random.randint(40 // 2, WIDTH - 40 // 2), 
                    -40 // 2)
            self.rect.center = center

    def draw(self):
        self.scale = pygame.transform.scale(self.image , (40, 40))
        self.surf = pygame.Surface((40, 40))
        center = (random.randint(40 // 2, WIDTH - 40 // 2), 
                  -40 // 2)
        self.rect = self.surf.get_rect(center=center)

# Creating our own event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

game_done = False
while not game_done:
    # Creating sprites
    enemy1 = Enemy()
    player1 = Player()
    star1 = star()
                

    #Creating Sprites Groups
    enemies = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    enemies.add(enemy1)
    stars.add(star1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(enemy1)


    score = 0
    done = False
    while not done:
        timer.tick(FPS)
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                game_done = True
            # if event.type == INC_SPEED:
            #     for sprite in all_sprites:
            #         sprite.speed += 100
       
        if not pygame.sprite.spritecollideany(player1, stars):
            for star in stars:
                DISPLAYSURF.blit(star.scale, star.rect)
                star.move()
        else:
            score += 1
            star1.draw()
            

        if pygame.sprite.spritecollideany(player1, enemies):
            pygame.mixer.Sound('crash.wav').play()
            DISPLAYSURF.fill(RED)
            txt_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            DISPLAYSURF.blit(game_over, txt_rect)
            pygame.display.flip()
            for sprite in all_sprites:
                sprite.kill()
        
            choosen = False
            while not choosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_done = True
                        choosen = True
                    if event.type == pygame.KEYDOWN:
                        choosen = True
                        if event.key == pygame.K_SPACE:
                            game_done = True
            done = True

        

        scores = font_small.render(str(score), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

        for sprite in all_sprites:
            sprite.move()
            sprite.draw(DISPLAYSURF)

        pygame.display.flip()
#Напишу кратко что сделал:
#1 - изменил класс звезды, там где функция отрисовки я убрал функцию surface.blit и отрисовывал ее в цикле. 
# А в саму функцию сделал почти копию того что написано в __init__. Так как там главный метод отрисовки, а отрисовывается она в цикле(162-164)
#2 - Изменил условие если не сталкиваются то звезда рисуется, а если сталкиваемся то увеличиваем очко и рисуем его (165-167)
pygame.quit()