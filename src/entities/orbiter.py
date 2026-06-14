import math
import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    ORBITER_SPEED, ORBITER_RADIUS, ORBITER_W, ORBITER_H,
    ORBITER_HP, ORBITER_POINTS, ORBITER_SHOOT_INTERVAL,
    SPRITE_ORBITER,
    ENEMY_PROJ_PLASMA, ENEMY_PROJ_PLASMA_W, ENEMY_PROJ_PLASMA_H,
)


class Orbiter(Enemy):
    def __init__(self, center_x: int, center_y: int, start_angle: float = 0.0):
        super().__init__(center_x, ORBITER_W, ORBITER_H, (100, 220, 180), ORBITER_HP, ORBITER_POINTS)
        raw = assets.get(SPRITE_ORBITER)
        self.image = pygame.transform.scale(raw, (ORBITER_W, ORBITER_H))
        self._cx = float(center_x)
        self._cy = float(center_y)
        self._angle = start_angle          # radianes
        self._angular_speed = math.radians(ORBITER_SPEED)  # rad/s
        self._recalc_pos()
        self.last_shot: int = -ORBITER_SHOOT_INTERVAL

    def _recalc_pos(self) -> None:
        self.x = self._cx + math.cos(self._angle) * ORBITER_RADIUS - ORBITER_W / 2
        self.y = self._cy + math.sin(self._angle) * ORBITER_RADIUS - ORBITER_H / 2
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def shoot(self, now: int) -> list:
        if now - self.last_shot < ORBITER_SHOOT_INTERVAL:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        cy = self.rect.centery
        target = getattr(self, "target", None)
        if target:
            dx = target.rect.centerx - cx
            dy = target.rect.centery - cy
            angle = math.degrees(math.atan2(dx, max(1, dy)))
        else:
            angle = 0
        return [EnemyBullet(cx, cy, angle, ENEMY_PROJ_PLASMA, ENEMY_PROJ_PLASMA_W, ENEMY_PROJ_PLASMA_H)]

    def update(self, dt: float) -> None:
        self._angle += self._angular_speed * dt
        self._recalc_pos()
        # No llamar super().update() — Orbiter nunca sale por pantalla verticalmente
        # Solo matar si hp <= 0 (ya gestionado por take_damage)
