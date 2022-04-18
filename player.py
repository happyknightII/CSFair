import math
import pygame

ACCELERATION = 0.3
MAX_SPEED = 100
MAX_TURN_SPEED = 8
MAX_AMMO = 50
RELOAD_SPEED = 100
FIRE_RATE = 150


class Player(pygame.sprite.Sprite):
    def __init__(self, bounds, scale):
        pygame.sprite.Sprite.__init__(self)
        self.bounds = bounds
        self.input = [0, 0]
        self.speed = [0, 0]
        self.pos = [bounds[0]/2, bounds[1]/2]
        self.angle = 0
        self.health = 100
        self.ammo = MAX_AMMO
        self.last_fired = pygame.time.get_ticks()
        self.last_reload = pygame.time.get_ticks()
        self.normalImage = pygame.transform.scale(pygame.image.load("png/player.png"), (scale, scale))
        self.damagedImage = pygame.transform.scale(pygame.image.load("png/playerDamaged.png"), (scale, scale))
        self.image = self.normalImage
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def move(self, x, axis):
        self.speed[axis] += x * ACCELERATION

    def rotate(self, pos):
        rel_x, rel_y = pos[0] - self.pos[0], pos[1] - self.pos[1]
        target_angle = (180 / math.pi) * math.atan2(rel_x, rel_y) + 180
        error = target_angle - self.angle
        if error < -180:
            error = 360 - error
        elif error > 180:
            error = - error
        self.angle %= 360
        if abs(error) > MAX_TURN_SPEED:
            error = MAX_TURN_SPEED * math.copysign(1, error)
        self.angle += error

    def fire(self):
        if pygame.time.get_ticks() - self.last_fired > FIRE_RATE and self.ammo > 0:
            self.ammo -= 1
            self.last_fired = pygame.time.get_ticks()
            return True
        else:
            return False

    def update(self):
        if self.ammo < MAX_AMMO and pygame.time.get_ticks() - self.last_reload > RELOAD_SPEED and pygame.time.get_ticks() - self.last_fired > 2 * FIRE_RATE:
            self.ammo += 1
            self.last_reload = pygame.time.get_ticks()
        if self.health > 50:
            self.image = pygame.transform.rotate(self.normalImage, self.angle)
        else:
            self.image = pygame.transform.rotate(self.damagedImage, self.angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        for i in range(2):
            if self.pos[i] < 0:
                self.speed[i] = 0.3 * abs(self.speed[i])
                self.pos[i] = 0
            elif self.pos[i] > self.bounds[i]:
                self.speed[i] = -0.3 * abs(self.speed[i])
                self.pos[i] = self.bounds[i]
            if abs(self.speed[i]) > MAX_SPEED:
                self.speed[i] = MAX_SPEED * math.copysign(1, self.speed[i])
            self.speed[i] *= .999
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.rect.center = self.pos
