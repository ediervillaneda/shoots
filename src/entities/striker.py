import math
import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    STRIKER_SPEED, STRIKER_W, STRIKER_H, STRIKER_HP, STRIKER_POINTS,
    STRIKER_SHOOT_INTERVAL, STRIKER_ENTRY_Y, SCREEN_W, SPRITE_STRIKER,
    ENEMY_PROJ_PROTON, ENEMY_PROJ_PROTON_W, ENEMY_PROJ_PROTON_H,
    PLAYER_SPEED, LEAD_TIME_S,
)


class Striker(Enemy):
    """Diagonal entry toward screen center, then straight down. Fires aimed bursts."""

    def __init__(self, x):
        super().__init__(x, STRIKER_W, STRIKER_H, (80, 160, 220), STRIKER_HP, STRIKER_POINTS)
        raw = assets.get(SPRITE_STRIKER)
        self.image = pygame.transform.scale(raw, (STRIKER_W, STRIKER_H))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(centerx=x, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self._dir_x: float = 1.0 if x < SCREEN_W // 2 else -1.0
        self.last_shot: int = -STRIKER_SHOOT_INTERVAL

    def shoot(self, now: int) -> list:
        if now - self.last_shot < STRIKER_SHOOT_INTERVAL:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        bottom = self.rect.bottom
        target = getattr(self, "target", None)
        if target:
            pred_x = target.rect.centerx + getattr(target, "vel_x", 0.0) * PLAYER_SPEED * LEAD_TIME_S
            pred_y = target.rect.centery + getattr(target, "vel_y", 0.0) * PLAYER_SPEED * LEAD_TIME_S
            dx = pred_x - cx
            dy = pred_y - bottom
            angle = math.degrees(math.atan2(dx, max(1, dy)))
        else:
            angle = 0
        return [
            EnemyBullet(cx, bottom, angle - 10, ENEMY_PROJ_PROTON, ENEMY_PROJ_PROTON_W, ENEMY_PROJ_PROTON_H),
            EnemyBullet(cx, bottom, angle + 10, ENEMY_PROJ_PROTON, ENEMY_PROJ_PROTON_W, ENEMY_PROJ_PROTON_H),
        ]

    def update(self, dt: float) -> None:
        speed = STRIKER_SPEED + getattr(self, "speed_bonus", 0.0)
        self.y += speed * dt
        if self.y < STRIKER_ENTRY_Y:
            self.x += self._dir_x * speed * 0.6 * dt
            self.x = max(0.0, min(float(SCREEN_W - STRIKER_W), self.x))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        super().update(dt)
