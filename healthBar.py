import pygame.sprite


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health=100, coord=(10, 10), ratio=10, bar_length=400, border=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((bar_length, bar_length / ratio))
        self.icon = pygame.transform.scale(pygame.image.load("png/life.png"), (bar_length / ratio, bar_length / ratio))
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        self.border = border
        self.max_health = max_health
        self.current_health = max_health
        print(self.rect.size[0] * self.current_health / self.max_health - self.border)

    def update(self):
        pygame.Surface.fill(self.image, (255, 255, 255))
        pygame.draw.rect(self.image, (255, 0, 0), (self.border,
                                                   self.border,
                                                   self.rect.size[0] - 2 * self.border,
                                                   self.rect.size[1] - 2 * self.border))
        if self.current_health > 0:
            pygame.draw.rect(self.image,
                             (0, 255, 0),
                             (self.border,
                              self.border,
                              self.rect.size[0] * self.current_health / self.max_health - 2 * self.border,
                              self.rect.size[1] - 2 * self.border))
        font = pygame.font.Font('freesansbold.ttf', int(self.rect.size[1] / 2))
        text = font.render(f'Health: {self.current_health}', True, (0, 0, 0))
        self.image.blit(text, (self.rect.size[0] / 4, self.rect.size[1] / 4))
        self.image.blit(self.icon, (self.rect.size[0] * self.current_health / self.max_health - 2 * self.border - self.rect.size[1] / 2, 0))
