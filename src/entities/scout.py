import pygame
from src.entities.enemy import Enemy
from src.settings import SCOUT_SPEED, SCOUT_COLOR, SCOUT_W, SCOUT_H, SCOUT_HP, SCOUT_POINTS


class Scout(Enemy):
    def __init__(self, x):
        super().__init__(x, SCOUT_W, SCOUT_H, SCOUT_COLOR, SCOUT_HP, SCOUT_POINTS)

    def update(self, dt):
        self.y += SCOUT_SPEED * dt
        self.rect.y = int(self.y)
        super().update(dt)
