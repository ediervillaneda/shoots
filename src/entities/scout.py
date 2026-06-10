import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.settings import SCOUT_SPEED, SCOUT_COLOR, SCOUT_W, SCOUT_H, SCOUT_HP, SCOUT_POINTS, SPRITE_SCOUT


class Scout(Enemy):
    def __init__(self, x):
        super().__init__(x, SCOUT_W, SCOUT_H, SCOUT_COLOR, SCOUT_HP, SCOUT_POINTS)
        raw = assets.get(SPRITE_SCOUT)
        self.image = pygame.transform.scale(raw, (SCOUT_W, SCOUT_H))
        self.image = pygame.transform.flip(self.image, False, True)

    def update(self, dt):
        self.y += (SCOUT_SPEED + getattr(self, "speed_bonus", 0.0)) * dt
        self.rect.y = int(self.y)
        super().update(dt)
