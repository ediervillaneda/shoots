import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    GUNNER_SPEED, GUNNER_W, GUNNER_H, GUNNER_HP, GUNNER_POINTS,
    GUNNER_SHOOT_INTERVAL, GUNNER_SPREAD_ANGLE, SPRITE_GUNNER,
)


class Gunner(Enemy):
    def __init__(self, x):
        super().__init__(x, GUNNER_W, GUNNER_H, (200, 120, 40), GUNNER_HP, GUNNER_POINTS)
        raw = assets.get(SPRITE_GUNNER)
        self.image = pygame.transform.scale(raw, (GUNNER_W, GUNNER_H))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(centerx=x, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.last_shot: int = -GUNNER_SHOOT_INTERVAL

    def shoot(self, now: int) -> list:
        if now - self.last_shot < GUNNER_SHOOT_INTERVAL:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        bottom = self.rect.bottom
        return [
            EnemyBullet(cx, bottom, -GUNNER_SPREAD_ANGLE),
            EnemyBullet(cx, bottom, 0),
            EnemyBullet(cx, bottom, GUNNER_SPREAD_ANGLE),
        ]

    def update(self, dt: float) -> None:
        self.y += (GUNNER_SPEED + getattr(self, "speed_bonus", 0.0)) * dt
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)
        super().update(dt)
