import pygame.sprite

ASPECT_RATIO = 9/33


class LaserBar(pygame.sprite.Sprite):
    def __init__(self, max_laser=50, coord=(10, 10), ratio=.1, bar_length=40, border=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((bar_length, bar_length / ratio))
        self.icon = pygame.transform.scale(pygame.image.load("png/laserRed.png"), (bar_length / ratio * ASPECT_RATIO, bar_length / ratio))
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        self.border = border
        self.max_level = max_laser
        self.current_level = max_laser
        print(self.rect.size[0] * self.current_level / self.max_level - self.border)

    def update(self):
        font = pygame.font.Font('freesansbold.ttf', int(self.rect.size[0] / 2))
        pygame.Surface.fill(self.image, (255, 255, 255))
        pygame.draw.rect(self.image, (255, 255, 0), (self.border,
                                                   self.border,
                                                   self.rect.size[0] - 2 * self.border,
                                                   self.rect.size[1] - 2 * self.border))
        if self.current_level > 0:
            pygame.draw.rect(self.image,
                             (255, 0, 0),
                             (self.border,
                              self.rect.size[1] * (1 - self.current_level / self.max_level) - 2 * self.border,
                              self.rect.size[0] - 2 * self.border,
                              self.rect.size[1] * self.current_level / self.max_level))
        text = font.render(f'Ammo: {self.current_level}', True, (0, 0, 0))
        self.image.blit(
            pygame.transform.rotate(text, 90),
            (self.rect.size[0] / 4, self.rect.size[1] / 2))
