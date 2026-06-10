import pygame
from src.settings import (
    ENEMY_BULLET_SPEED, ENEMY_BULLET_COLOR,
    ENEMY_BULLET_W, ENEMY_BULLET_H, SCREEN_H,
)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_BULLET_W, ENEMY_BULLET_H))
        self.image.fill(ENEMY_BULLET_COLOR)
        self.rect = self.image.get_rect(centerx=x, top=y)  # top anchored so bullet tip starts at muzzle
        self.y = float(self.rect.y)

    def update(self, dt):
        self.y += ENEMY_BULLET_SPEED * dt
        self.rect.y = int(self.y)
        if self.rect.top > SCREEN_H:
            self.kill()
