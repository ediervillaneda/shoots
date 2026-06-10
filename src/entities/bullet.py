import pygame
from src.settings import BULLET_SPEED, BULLET_COLOR, BULLET_W, BULLET_H


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_W, BULLET_H))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.y = float(self.rect.y)

    def update(self, dt):
        self.y -= BULLET_SPEED * dt
        self.rect.y = int(self.y)
        if self.rect.bottom < 0:
            self.kill()
