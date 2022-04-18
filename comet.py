import random
import pygame.sprite

ASPECT_RATIO_LARGE = 136/111
MULTIPLIER_LARGE = 136 / 44
ASPECT_RATIO_SMALL = 44/42

MAX_SPEED = 2


class Comet(pygame.sprite.Sprite):
    def __init__(self, bounds, big, size):
        pygame.sprite.Sprite.__init__(self)
        self.bounds = bounds
        self.spin = random.random() * 9
        self.angle = 0
        self.speed = [random.random() * MAX_SPEED + MAX_SPEED * 0.1, random.random() * MAX_SPEED + MAX_SPEED * 0.1]
        if random.random() > 0.25:
            self.pos = [-bounds[0] * 0.1, random.randint(0, bounds[1])]
        elif random.random() > 0.5:
            self.pos = [random.randint(0, bounds[0]), -bounds[1] * 0.1]
        elif random.random() > 0.75:
            self.pos = [bounds[0] * 1.1, random.randint(0, bounds[1])]
        else:
            self.pos = [random.randint(0, bounds[0]), bounds[1] * 1.1]
        if big:
            self.sourceImage = pygame.transform.scale(pygame.image.load("png/meteorBig.png"), (MULTIPLIER_LARGE * size * ASPECT_RATIO_LARGE, MULTIPLIER_LARGE * size))

        else:
            self.sourceImage = pygame.transform.scale(pygame.image.load("png/meteorBig.png"), (size * ASPECT_RATIO_SMALL, size))
        self.image = self.sourceImage
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.angle += self.spin
        self.angle %= 360
        self.image = pygame.transform.rotate(self.sourceImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)
        for i in range(2):
            self.pos[i] += self.speed[i]
            if self.pos[i] < -self.bounds[0] * 0.2 or self.pos[i] > self.bounds[0] * 1.2:
                self.kill()
