import pygame
import random as rd

pygame.init()

#colours
black = (0, 0, 0)
white = (230, 230, 230)
red = (255, 0, 0)
green = (80, 255, 20)
blue = (60, 80, 255)
grey = (160, 160, 160)

#const
width = 1840
height = 920
fps = 30

population = 350
people = [0] * population
speeds = (-3, -2, 2, 3)

#setting display
display = pygame.display.set_mode((width, height))
pygame.display.update()
pygame.display.set_caption('Covid simulation')
clock = pygame.time.Clock()

ppl = pygame.sprite.Group()
inf = pygame.sprite.Group()
rec = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Human(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8, 8))
        self.image.fill(blue)
        self.rect = pygame.Surface((20, 20)).get_rect()
        self.time = 0

        #coordinates
        self.rect.x = rd.randint(0, width)
        self.rect.y = rd.randint(0, height)

        self.infected = False
        self.recovered = False
        self.dead = False

        #setting speed
        global speeds
        x_speed = rd.choice(speeds)
        y_speed = rd.choice(speeds)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        if self.rect.x >= width:
            self.x_speed = - self.x_speed

        elif self.rect.x <= 0:
            self.x_speed = - self.x_speed

        if self.rect.y >= height:
            self.y_speed = - self.y_speed

        elif self.rect.y <= 0:
            self.y_speed = - self.y_speed

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        global inf

        if self.infected and not self.recovered:
            self.image.fill(red)
            self.time += 1

            if self.time >= 140:
                self.infected = False
                self.recovered = True
                self.time = 0
                if rd.random() <= 0.04:
                    self.x_speed = 0
                    self.y_speed = 0
                    self.dead = True
                    self.image.fill(black)

        elif self.recovered and not self.dead:
            self.image.fill(green)
            self.time += 1

            if self.time >= 400:
                self.recovered = False
                self.time = 0

        elif self.dead:
            pygame.Surface((12, 12)).fill(black)

        else:
            self.image.fill(blue)

            for i in inf:
                if self.rect.colliderect(i) and rd.random() <= 0.3:
                    self.infected = True

for i in range(population):
    human = Human()
    if i == 0:
        human.infected = True
    if human.infected:
        inf.add(human)
    else:
        ppl.add(human)
    all_sprites.add(human)

#main cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for sprite in all_sprites:
        if sprite.infected:
            inf.add(sprite)
            rec.remove(sprite)
            ppl.remove(sprite)
        elif not sprite.infected and sprite.recovered:
            rec.add(sprite)
            inf.remove(sprite)
            ppl.remove(sprite)
        else:
            ppl.add(sprite)
            inf.remove(sprite)
            rec.remove(sprite)

    clock.tick(fps)
    all_sprites.update()

    display.fill(white)
    all_sprites.draw(display)

    pygame.display.flip()

pygame.quit()
quit()