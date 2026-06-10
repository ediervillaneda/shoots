import math
import pygame
from src.entities.enemy import Enemy
from src.settings import (
    FIGHTER_SPEED, FIGHTER_COLOR, FIGHTER_W, FIGHTER_H,
    FIGHTER_HP, FIGHTER_POINTS, FIGHTER_AMPLITUDE, FIGHTER_FREQUENCY,
)


class Fighter(Enemy):
    def __init__(self, x):
        super().__init__(x, FIGHTER_W, FIGHTER_H, FIGHTER_COLOR, FIGHTER_HP, FIGHTER_POINTS)
        self.origin_x = float(self.rect.x)
        self.elapsed = 0.0

    def update(self, dt):
        self.elapsed += dt
        self.y += FIGHTER_SPEED * dt
        offset = math.sin(self.elapsed * FIGHTER_FREQUENCY * 2 * math.pi) * FIGHTER_AMPLITUDE
        self.x = self.origin_x + offset
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        super().update(dt)
