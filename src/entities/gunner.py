import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    GUNNER_SPEED, GUNNER_W, GUNNER_H, GUNNER_HP, GUNNER_POINTS,
    GUNNER_SPREAD_ANGLE, SPRITE_GUNNER,
    ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H,
    BURST_COUNT, BURST_INTERVAL_MS, BURST_PAUSE_MS,
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
        self._burst_idx: int = 0        # cuántas balas de la ráfaga se han disparado
        self._next_burst_ms: int = 0    # pygame.time.get_ticks() del próximo disparo

    def shoot(self, now: int) -> list:
        if now < self._next_burst_ms:
            return []
        cx = self.rect.centerx
        bottom = self.rect.bottom
        bullets = [
            EnemyBullet(cx, bottom, -GUNNER_SPREAD_ANGLE, ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
            EnemyBullet(cx, bottom, 0,                    ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
            EnemyBullet(cx, bottom,  GUNNER_SPREAD_ANGLE, ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
        ]
        self._burst_idx += 1
        if self._burst_idx >= BURST_COUNT:
            self._burst_idx = 0
            self._next_burst_ms = now + BURST_PAUSE_MS
        else:
            self._next_burst_ms = now + BURST_INTERVAL_MS
        return bullets

    def update(self, dt: float) -> None:
        self.y += (GUNNER_SPEED + getattr(self, "speed_bonus", 0.0)) * dt
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)
        super().update(dt)
