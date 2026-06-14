import math
import pygame
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    HOMING_TURN_SPEED, HOMING_BULLET_SPEED,
    ENEMY_PROJ_PLASMA, ENEMY_PROJ_PLASMA_W, ENEMY_PROJ_PLASMA_H,
    ENEMY_PROJ_FRAME_MS,
)


class HomingBullet(EnemyBullet):
    def __init__(self, x: int, y: int, angle_deg: float, target, frames=None, w=None, h=None):
        super().__init__(x, y, angle_deg, frames, w, h)
        # Sobrescribir velocidad con HOMING_BULLET_SPEED (más lenta que normal)
        rad = math.radians(angle_deg)
        self._vx = math.sin(rad) * HOMING_BULLET_SPEED
        self._vy = math.cos(rad) * HOMING_BULLET_SPEED
        self._target = target

    def update(self, dt: float) -> None:
        if self._target and self._target.alive():
            # Ángulo actual
            current_angle = math.degrees(math.atan2(self._vx, self._vy))
            # Ángulo hacia target
            dx = self._target.rect.centerx - self.rect.centerx
            dy = self._target.rect.centery - self.rect.centery
            desired_angle = math.degrees(math.atan2(dx, max(1, dy)))
            # Diferencia angular (normalizar a [-180, 180])
            diff = (desired_angle - current_angle + 180) % 360 - 180
            # Limitar corrección a HOMING_TURN_SPEED * dt
            max_turn = HOMING_TURN_SPEED * dt
            turn = max(-max_turn, min(max_turn, diff))
            new_angle = current_angle + turn
            rad = math.radians(new_angle)
            self._vx = math.sin(rad) * HOMING_BULLET_SPEED
            self._vy = math.cos(rad) * HOMING_BULLET_SPEED
        super().update(dt)
