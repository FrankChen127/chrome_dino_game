import pygame
import neat
import time
import os
import random
import math

bard1 = pygame.image.load("data/berd.png")
bard2 = pygame.image.load("data/berd2.png")
bard1 = pygame.transform.scale(bard1, (85, 70))
bard2 = pygame.transform.scale(bard2, (85, 70))
bard = [bard1, bard2]
cactus_pics = [pygame.image.load("data/cactusBig0000.png"), pygame.image.load("data/cactusSmall0000.png"),
               pygame.image.load("data/cactusSmallMany0000.png")]
dino_low1 = pygame.image.load("data/dinoduck0000.png")
dino_low1 = pygame.transform.scale(dino_low1, (125, 57))
dino_low2 = pygame.image.load("data/dinoduck0001.png")
dino_low2 = pygame.transform.scale(dino_low2, (125, 57))
dino_low = [dino_low1, dino_low2]
dino_run = [pygame.image.load("data/dinorun0000.png"), pygame.image.load("data/dinorun0001.png")]
dino_jump = pygame.image.load("data/dinojump0000.png")
dino_dead = pygame.image.load("data/dinoDead0000.png")
dino_dead = pygame.transform.scale(dino_dead, (96, 100))

GROUND_Y = 430
WIN_SIZE = (800, 500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Dino(object):
    def __init__(self):
        self.x = 85
        self.y = GROUND_Y - 110
        self.force = 0
        self.velocity = 9
        self.mass = 1
        self.run = True
        self.run_count = 0
        self.is_low = False
        self.is_jump = False
        self.is_jump_low = False
        self.width = 96
        self.height = 112
        global alive
        self.hit_box1 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hit_box2 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hit_box3 = pygame.Rect(self.x, self.y, self.width, self.height)

    def change_is_jump(self):
        self.is_jump = True
        self.run = False
        self.width = 96
        self.height = 100

    def change_is_low(self):
        self.is_low = True

    def change_is_jump_low(self):
        self.is_jump_low = True
        self.force = 90
        if self.velocity > 0:
            self.velocity = 0

    def jump(self):
        self.force = 0.5 * self.mass * (self.velocity ** 2)
        self.y -= self.force
        self.velocity -= 1
        if self.velocity < 0:
            self.mass = -1
        if self.y >= GROUND_Y - 110:
            self.is_jump = False
            self.velocity = 9
            self.mass = 1
            self.is_jump_low = False
            self.y = GROUND_Y - 110

    def print(self):
        self.width = 96
        self.height = 112
        if not alive:
            window.blit(dino_dead, (self.x, self.y))
        elif self.is_jump:
            self.hit_box1 = pygame.Rect(self.x + 46, self.y, self.width - 46, 50)
            self.hit_box2 = pygame.Rect(self.x + 10, self.y + 45, self.width - 30, self.height - 65)
            self.hit_box3 = pygame.Rect(self.x + 10, self.y + 45, self.width - 30, self.height - 65)
            window.blit(dino_jump, (self.x, self.y))
        elif self.is_low:
            self.width = 125
            self.height = 57
            self.hit_box1 = pygame.Rect(self.x, self.y + 55, self.width, self.height)
            self.hit_box2 = pygame.Rect(self.x, self.y + 55, self.width, self.height)
            self.hit_box3 = pygame.Rect(self.x, self.y + 55, self.width, self.height)
            if self.run_count < 3:
                window.blit(dino_low[0], (self.x, self.y + 50))
                self.run_count += 1
            else:
                window.blit(dino_low[1], (self.x, self.y + 50))
                self.run_count += 1
            if self.run_count >= 6:
                self.run_count = 0
        else:
            self.hit_box1 = pygame.Rect(self.x + 45, self.y, self.width - 45, 50)
            self.hit_box2 = pygame.Rect(self.x, self.y + 50, self.width - 30, self.height - 70)
            self.hit_box3 = pygame.Rect(self.x + 20, self.y + 80, self.width - 60, self.height - 87)
            if self.run_count < 3:
                window.blit(dino_run[0], (self.x, self.y))
                self.run_count += 1
            else:
                window.blit(dino_run[1], (self.x, self.y))
                self.run_count += 1
            if self.run_count >= 6:
                self.run_count = 0
        # pygame.draw.rect(window, BLACK, self.hit_box1, 2)
        # pygame.draw.rect(window, (255, 0, 0), self.hit_box2, 2)
        # pygame.draw.rect(window, (255, 0, 0), self.hit_box3, 2)


class Cactus(object):
    def __init__(self):
        self.velocity = 0.0
        self.x = 1000
        self.y = GROUND_Y
        self.kind = 0
        self.width = 0
        self.height = 0
        self.x_plus = 0
        self.hit_box1 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hit_box2 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hit_box3 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.generate(2300)

    def generate(self, x=0):
        self.kind = random.randrange(0, 3)
        self.x_plus = random.randrange(0, 200)
        self.x = 800 + self.x_plus + x
        self.y = GROUND_Y - 110
        if self.kind == 0:
            self.width = 60
            self.height = 120
            self.hit_box1 = pygame.Rect(self.x, self.y + 15, self.width, self.height - 15)
            self.hit_box2 = pygame.Rect(self.x + 10, self.y, self.width, self.height)
            self.hit_box3 = pygame.Rect(self.x + 20, self.y + 20, self.width, self.height - 20)
        elif self.kind == 1:
            self.width = 40
            self.height = 80
            self.y += 30
        else:
            self.width = 120
            self.height = 80
            self.y += 30

    def move(self, speed):
        if self.x > 0 - self.width:
            self.x -= speed
        else:
            self.generate()

    def print(self):
        window.blit(cactus_pics[self.kind], (self.x, self.y))
        if self.kind == 0:
            self.hit_box1 = pygame.Rect(self.x, self.y + 20, self.width / 3, self.height - 20)
            self.hit_box2 = pygame.Rect(self.x + 10, self.y, self.width / 3, self.height)
            self.hit_box3 = pygame.Rect(self.x + 40, self.y + 30, self.width / 3, self.height - 40)
        elif self.kind == 1:
            self.hit_box1 = pygame.Rect(self.x, self.y + 20, self.width / 3, self.height - 20)
            self.hit_box2 = pygame.Rect(self.x + 10, self.y, self.width / 3, self.height)
            self.hit_box3 = pygame.Rect(self.x + 27, self.y + 19, self.width / 3, self.height - 40)
        else:
            self.hit_box1 = pygame.Rect(self.x, self.y, self.width, self.height)
            self.hit_box2 = pygame.Rect(self.x, self.y, self.width, self.height)
            self.hit_box3 = pygame.Rect(self.x, self.y, self.width, self.height)


class Bird(object):
    def __init__(self):
        self.height = 80
        self.width = 92
        self.kind = 0  # 0 or 1
        self.x = 10000
        self.y = 0
        self.speed = 0
        self.plus_x = 0
        self.hit_box1 = pygame.Rect(self.x, self.y, 80, 92)
        self.hit_box2 = pygame.Rect(self.x, self.y, 80, 92)
        self.generate(40000)
        self.run_count = 0

    def generate(self, x=5000):
        self.kind = random.randrange(0, 2)
        self.plus_x = random.randrange(0, 300)
        self.x = x + self.plus_x
        if self.kind == 0:
            self.y = 280
        else:
            self.y = 230

    def move(self, velocity):
        if self.x < 0:
            self.generate()
        else:
            self.x -= velocity

    def print(self):
        if self.run_count < 3:
            self.hit_box1 = pygame.Rect(self.x, self.y + 7, 30, 30)
            self.hit_box2 = pygame.Rect(self.x + 30, self.y+10, 40, 50)
            window.blit(bard[0], (self.x, self.y))
            self.run_count += 1
        else:
            self.hit_box1 = pygame.Rect(self.x, self.y + 7, 30, 30)
            self.hit_box2 = pygame.Rect(self.x + 30, self.y+10, 40, 50)
            window.blit(bard[1], (self.x, self.y))
            self.run_count += 1
        if self.run_count >= 6:
            self.run_count = 0
        #pygame.draw.rect(window, BLACK, self.hit_box1, 2)
        #pygame.draw.rect(window, (255, 0, 0), self.hit_box2, 2)


def distance():
    if cactus.x > bird.x and (cactus.x - bird.x) < 200:
        cactus.x += 300
    if cactus.x < bird.x and (bird.x - cactus.x) < 200:
        bird.x += 300


def hit(rounds):
    if pygame.Rect.colliderect(dino.hit_box1, bird.hit_box1) or pygame.Rect.colliderect(dino.hit_box2,bird.hit_box1) or pygame.Rect.colliderect(dino.hit_box3, bird.hit_box1) or pygame.Rect.colliderect(dino.hit_box1,cactus.hit_box1) or pygame.Rect.colliderect(dino.hit_box1, cactus.hit_box2) or pygame.Rect.colliderect(dino.hit_box1,cactus.hit_box3) or pygame.Rect.colliderect(dino.hit_box2, cactus.hit_box1) or pygame.Rect.colliderect(dino.hit_box2,cactus.hit_box2) or pygame.Rect.colliderect(dino.hit_box2, cactus.hit_box3) or pygame.Rect.colliderect(dino.hit_box3,cactus.hit_box1) or pygame.Rect.colliderect(dino.hit_box3, cactus.hit_box2) or pygame.Rect.colliderect(dino.hit_box3,cactus.hit_box3) or pygame.Rect.colliderect(dino.hit_box1, bird.hit_box2) or pygame.Rect.colliderect(dino.hit_box2,bird.hit_box2) or pygame.Rect.colliderect(dino.hit_box3, bird.hit_box2):
        return False, rounds+1
    else:
        return True, rounds


def reload_window(score, round, hi, font1):
    window.fill(WHITE)
    dino.print()
    cactus.print()
    bird.print()
    if round >= 1:
        text = font1.render("Hi: ", False, BLACK)
        window.blit(text, (550, 20))
        text = font1.render(str(hi), False, BLACK)
        window.blit(text, (570, 20))
    num = font1.render("Score: ", False, BLACK)
    window.blit(num, (630, 20))
    num = font1.render(str(score), False, BLACK)
    window.blit(num, (700, 20))
    pygame.draw.line(window, BLACK, (0, GROUND_Y), (1000, GROUND_Y), 2)
    dino.is_low = False
    pygame.display.update()


# variables
speed = 18
run = True
alive = False
score = 0
t = 0
high_score = []
round = 0
hi = 0

dino = Dino()
cactus = Cactus()
bird = Bird()

# window set up
pygame.init()
window = pygame.display.set_mode(WIN_SIZE)
window.fill(WHITE)
pygame.display.update()
font1 = pygame.font.Font(pygame.font.get_default_font(), 16)
font2 = pygame.font.Font(pygame.font.get_default_font(), 32)
clock = pygame.time.Clock()
# main loop
while run:
    if alive:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        if down:
            dino.change_is_low()
        elif not dino.is_jump:
            if key[pygame.K_SPACE] or key[pygame.K_UP]:
                dino.change_is_jump()
        if dino.is_low and dino.is_jump and not dino.is_jump_low:
            dino.change_is_jump_low()
        if dino.is_jump:
            dino.jump()

        speed += 0.003
        cactus.move(speed)
        bird.move(speed)
        distance()
        alive, round = hit(round)
        score += 1
        reload_window(score, round, hi, font1)
    else:
        high_score.append(score)
        high_score.sort()
        hi = high_score[len(high_score) - 1]
        button = pygame.Rect(300, 200, 160, 50)
        pygame.draw.rect(window, BLACK, button, 2)
        if round == 0:
            text = font2.render("Start", False, BLACK)
            window.blit(text, (340, 215))
        else:
            text = font2.render("Try Again", False, BLACK)
            window.blit(text, (307, 215))
        pygame.display.update()
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.collidepoint(event.pos):
                        alive = True
                        speed = 18
                        dino = Dino()
                        cactus = Cactus()
                        bird = Bird()
                        score = 0
            elif key[pygame.K_SPACE] or key[pygame.K_UP]:
                alive = True
                speed = 18
                dino = Dino()
                cactus = Cactus()
                bird = Bird()
                score = 0
pygame.quit()
