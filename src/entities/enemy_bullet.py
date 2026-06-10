import math
import pygame
import src.assets as assets
from src.settings import (
    ENEMY_BULLET_SPEED,
    ENEMY_BULLET_W, ENEMY_BULLET_H, SCREEN_H, SCREEN_W, SPRITE_FIGHTER_BULLET,
)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, angle_deg: float = 0):
        super().__init__()
        raw = assets.get(SPRITE_FIGHTER_BULLET)
        self.image = pygame.transform.scale(raw, (ENEMY_BULLET_W, ENEMY_BULLET_H))
        self.rect = self.image.get_rect(centerx=x, top=y)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        rad = math.radians(angle_deg)
        self._vx: float = math.sin(rad) * ENEMY_BULLET_SPEED
        self._vy: float = math.cos(rad) * ENEMY_BULLET_SPEED

    def update(self, dt: float) -> None:
        self.x += self._vx * dt
        self.y += self._vy * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.rect.top > SCREEN_H or self.rect.right < 0 or self.rect.left > SCREEN_W:
            self.kill()
