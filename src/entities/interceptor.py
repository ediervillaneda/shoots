import math
import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    INTERCEPTOR_SPEED, INTERCEPTOR_W, INTERCEPTOR_H, INTERCEPTOR_HP, INTERCEPTOR_POINTS,
    INTERCEPTOR_SHOOT_INTERVAL, INTERCEPTOR_Y_TARGET, INTERCEPTOR_PATROL_SPEED,
    SCREEN_W, SPRITE_INTERCEPTOR,
    ENEMY_PROJ_PLASMA, ENEMY_PROJ_PLASMA_W, ENEMY_PROJ_PLASMA_H,
)


class Interceptor(Enemy):
    """Fast entry to patrol row, then ping-pong + rapid aimed fire."""

    def __init__(self, x):
        super().__init__(x, INTERCEPTOR_W, INTERCEPTOR_H, (220, 60, 180), INTERCEPTOR_HP, INTERCEPTOR_POINTS)
        raw = assets.get(SPRITE_INTERCEPTOR)
        self.image = pygame.transform.scale(raw, (INTERCEPTOR_W, INTERCEPTOR_H))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(centerx=x, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self._entry_done: bool = False
        self._dir_x: float = 1.0 if x < SCREEN_W // 2 else -1.0
        self.last_shot: int = -INTERCEPTOR_SHOOT_INTERVAL

    def shoot(self, now: int) -> list:
        if not self._entry_done:
            return []
        if now - self.last_shot < INTERCEPTOR_SHOOT_INTERVAL:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        bottom = self.rect.bottom
        target = getattr(self, "target", None)
        if target:
            dx = target.rect.centerx - cx
            dy = target.rect.centery - bottom
            angle = math.degrees(math.atan2(dx, max(1, dy)))
        else:
            angle = 0
        return [EnemyBullet(cx, bottom, angle, ENEMY_PROJ_PLASMA, ENEMY_PROJ_PLASMA_W, ENEMY_PROJ_PLASMA_H)]

    def update(self, dt: float) -> None:
        speed = INTERCEPTOR_SPEED + getattr(self, "speed_bonus", 0.0)
        if not self._entry_done:
            self.y += speed * dt
            if self.y >= INTERCEPTOR_Y_TARGET:
                self.y = float(INTERCEPTOR_Y_TARGET)
                self._entry_done = True
        else:
            self.x += INTERCEPTOR_PATROL_SPEED * self._dir_x * dt
            if self.rect.right >= SCREEN_W:
                self._dir_x = -1.0
                self.rect.right = SCREEN_W
                self.x = float(self.rect.x)
            elif self.rect.left <= 0:
                self._dir_x = 1.0
                self.rect.left = 0
                self.x = float(self.rect.x)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        # skip Enemy.update: patrol row is above SCREEN_H, would never self-kill by y
