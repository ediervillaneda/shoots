import math
import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.settings import KAMIKAZE_SPEED, KAMIKAZE_W, KAMIKAZE_H, KAMIKAZE_HP, KAMIKAZE_POINTS


class Kamikaze(Enemy):
    def __init__(self, x):
        super().__init__(x, KAMIKAZE_W, KAMIKAZE_H, (180, 50, 220), KAMIKAZE_HP, KAMIKAZE_POINTS)
        raw = assets.get("ship/insect-1.png")
        self.image = pygame.transform.scale(raw, (KAMIKAZE_W, KAMIKAZE_H))
        self.rect = self.image.get_rect(centerx=x, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, dt):
        speed = KAMIKAZE_SPEED + getattr(self, "speed_bonus", 0.0)
        target = getattr(self, "target", None)
        if target:
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            dist = max(1.0, math.hypot(dx, dy))
            self.x += (dx / dist) * speed * dt
            self.y += (dy / dist) * speed * dt
        else:
            self.y += speed * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        super().update(dt)
