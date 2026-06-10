import pygame
import src.assets as assets
from src.settings import (
    ENEMY_BULLET_SPEED,
    ENEMY_BULLET_W, ENEMY_BULLET_H, SCREEN_H, SPRITE_FIGHTER_BULLET,
)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        raw = assets.get(SPRITE_FIGHTER_BULLET)
        self.image = pygame.transform.scale(raw, (ENEMY_BULLET_W, ENEMY_BULLET_H))
        self.rect = self.image.get_rect(centerx=x, top=y)
        self.y = float(self.rect.y)

    def update(self, dt):
        self.y += ENEMY_BULLET_SPEED * dt
        self.rect.y = int(self.y)
        if self.rect.top > SCREEN_H:
            self.kill()
