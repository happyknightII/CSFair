import math
import random
import pygame

ACCELERATION = 0.5
MAX_SPEED = 3
MAX_TURN_SPEED = 8
EXPLOSION_TIME = 10
CHANGE_RATE = 500


class Enemy(pygame.sprite.Sprite):
    def __init__(self, bounds, scale):
        pygame.sprite.Sprite.__init__(self)
        self.bounds = bounds
        self.current_action = 0
        self.lastActionTime = 0
        self.pattern = random.sample(range(0, 12), 12)
        self.pattern = [x % 4 for x in self.pattern]
        self.canShoot = True
        self.speed = [0, 0]
        if random.random() > 0.25:
            self.pos = [-bounds[0] * 0.1, random.randint(0, bounds[1])]
        elif random.random() > 0.5:
            self.pos = [random.randint(0, bounds[0]), -bounds[1] * 0.1]
        elif random.random() > 0.75:
            self.pos = [bounds[0] * 1.1, random.randint(0, bounds[1])]
        else:
            self.pos = [random.randint(0, bounds[0]), bounds[1] * 1.1]
        self.angle = 0
        self.dying = EXPLOSION_TIME

        self.sourceImage = pygame.transform.scale(pygame.image.load("png/enemyShip.png"), (scale, scale))
        self.blast = pygame.transform.scale(pygame.image.load("png/laserRedShot.png"), (scale, scale))
        self.image = self.sourceImage
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.lastFired = pygame.time.get_ticks()

    def move(self, x):
        action = self.pattern[x]
        self.speed[0] += ACCELERATION * 0.5 if action % 2 == 0 else -0.5
        self.speed[1] += ACCELERATION * 0.5 if (action / 2) == 0 else 0.3

    def rotate(self, pos):
        rel_x, rel_y = pos[0] - self.pos[0], pos[1] - self.pos[1]
        target_angle = (180 / math.pi) * math.atan2(rel_x, rel_y)
        self.angle = target_angle

    def collide(self):
        self.image = self.blast
        self.speed = [0, 0]
        self.dying -= 1

    def update(self, player_pos):
        if self.dying < EXPLOSION_TIME:
            self.dying -= 1
            if self.dying < 0:
                self.kill()
        else:
            if pygame.time.get_ticks() - self.lastActionTime > CHANGE_RATE:
                self.current_action += 1
                self.current_action %= 4
                self.lastActionTime = pygame.time.get_ticks()
            self.move(self.current_action)
            self.rotate(player_pos)
            self.image = pygame.transform.rotate(self.sourceImage, self.angle)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            for i in range(2):
                if self.pos[i] < 0:
                    self.pos[i] = 1
                    self.speed[i] = 0.3 * abs(self.speed[i])
                elif self.pos[i] > self.bounds[i]:
                    self.pos[i] = self.bounds[i] - 1
                    self.speed[i] = -0.3 * abs(self.speed[i])
                if abs(self.speed[i]) > MAX_SPEED:
                    self.speed[i] = MAX_SPEED * math.copysign(1, self.speed[i])
                self.speed[i] *= .999
            self.pos[0] += math.cos(math.radians(self.angle)) * self.speed[0] + math.sin(math.radians(self.angle)) * self.speed[1]
            self.pos[1] += math.sin(math.radians(self.angle)) * self.speed[0] + math.cos(math.radians(self.angle)) * self.speed[1]
        self.rect.center = self.pos
