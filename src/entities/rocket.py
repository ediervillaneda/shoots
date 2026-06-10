import math
import pygame
import src.assets as assets
from src.settings import ROCKET_SPEED, ROCKET_W, ROCKET_H, SPRITE_ROCKET, SCREEN_W


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, angle_deg: float = 0.0):
        super().__init__()
        raw = assets.get(SPRITE_ROCKET)
        scaled = pygame.transform.scale(raw, (ROCKET_W, ROCKET_H))
        # pygame.transform.rotate: positive = CCW; negate for CW (rightward lean)
        self.image = pygame.transform.rotate(scaled, -angle_deg)
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        angle_rad = math.radians(angle_deg)
        self.vx = ROCKET_SPEED * math.sin(angle_rad)
        self.vy = -ROCKET_SPEED * math.cos(angle_rad)

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > SCREEN_W:
            self.kill()
