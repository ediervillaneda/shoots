import pygame
import src.assets as assets
from src.settings import POWERUP_SPEED, POWERUP_W, POWERUP_H, SCREEN_H

POWERUP_ASSETS = {
    "rapid_fire":  "ship/bonus_time.png",
    "shield":      "ship/bonus_shield.png",
    "double_shot": "ship/laser-2.png",
    "triple_shot": "ship/laser-3.png",
    "extra_life":  "ship/bonus_life.png",
}

POWERUP_KINDS = list(POWERUP_ASSETS)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind: str, x: int, y: int):
        super().__init__()
        raw = assets.get(POWERUP_ASSETS[kind])
        self.image = pygame.transform.scale(raw, (POWERUP_W, POWERUP_H))
        self.rect = self.image.get_rect(centerx=x, top=y)
        self.y = float(self.rect.y)
        self.kind = kind

    def update(self, dt):
        self.y += POWERUP_SPEED * dt
        self.rect.y = int(self.y)
        if self.rect.top > SCREEN_H:
            self.kill()
