import math

import pygame.sprite

ASPECT_RATIO = 9/33
EXPLOSION_TIME = 10


class Laser(pygame.sprite.Sprite):
    def __init__(self, bounds, size, coord, angle, offset_speed, friendly, speed=20):
        pygame.sprite.Sprite.__init__(self)
        self.bounds = bounds
        self.angle = -angle - 90
        self.offset_speed = [offset_speed[0], offset_speed[1]]
        self.speed = (math.cos(math.radians(self.angle)) * speed,
                      math.sin(math.radians(self.angle)) * speed)
        if friendly:
            self.image = pygame.image.load("png/laserRed.png")
            self.blast = pygame.image.load("png/laserRedShot.png")
        else:
            self.image = pygame.image.load("png/laserGreen.png")
            self.blast = pygame.image.load("png/laserGreenShot.png")
        self.image = pygame.transform.scale(self.image, (size * ASPECT_RATIO, size))
        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.mask = self.mask = pygame.mask.from_surface(self.image)
        self.pos = [coord[0], coord[1]]
        self.rect.center = self.pos
        self.dying = EXPLOSION_TIME

    def collide(self):
        self.image = self.blast
        self.speed = [0, 0]
        self.dying -= 1

    def update(self):
        if self.dying < EXPLOSION_TIME:
            self.dying -= 1
            if self.dying < 0:
                self.kill()
        else:
            self.rect.center = self.pos
            for i in range(2):
                self.pos[i] += self.speed[i] + self.offset_speed[i]
                if self.pos[i] < -self.bounds[0] * 0.1 or self.pos[i] > self.bounds[0] * 1.1:
                    self.kill()

