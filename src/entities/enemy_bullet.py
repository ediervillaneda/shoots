import math
import pygame
import src.assets as assets
from src.settings import (
    ENEMY_BULLET_SPEED,
    SCREEN_H, SCREEN_W,
    ENEMY_PROJ_PLASMA, ENEMY_PROJ_PLASMA_W, ENEMY_PROJ_PLASMA_H,
    ENEMY_PROJ_FRAME_MS,
)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        angle_deg: float = 0,
        frames: list[str] | None = None,
        w: int | None = None,
        h: int | None = None,
    ):
        super().__init__()
        if frames is None:
            frames = ENEMY_PROJ_PLASMA
        if w is None:
            w = ENEMY_PROJ_PLASMA_W
        if h is None:
            h = ENEMY_PROJ_PLASMA_H

        self._frames = [pygame.transform.scale(assets.get(p), (w, h)) for p in frames]
        self._idx = 0
        self._timer = 0.0
        self.image = self._frames[0]
        self.rect = self.image.get_rect(centerx=x, top=y)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        rad = math.radians(angle_deg)
        self._vx: float = math.sin(rad) * ENEMY_BULLET_SPEED
        self._vy: float = math.cos(rad) * ENEMY_BULLET_SPEED

    def update(self, dt: float) -> None:
        self._timer += dt * 1000
        while self._timer >= ENEMY_PROJ_FRAME_MS:
            self._timer -= ENEMY_PROJ_FRAME_MS
            self._idx = (self._idx + 1) % len(self._frames)
            self.image = self._frames[self._idx]

        self.x += self._vx * dt
        self.y += self._vy * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.rect.top > SCREEN_H or self.rect.right < 0 or self.rect.left > SCREEN_W:
            self.kill()
