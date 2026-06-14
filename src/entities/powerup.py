import pygame
import src.assets as assets
from src.settings import (
    POWERUP_SPEED, POWERUP_W, POWERUP_H, SCREEN_H,
    SPRITE_PU_RAPID_FIRE, SPRITE_PU_SHIELD, SPRITE_PU_DOUBLE_SHOT,
    SPRITE_PU_EXTRA_LIFE, SPRITE_PU_ROCKET,
)

POWERUP_ASSETS = {
    "rapid_fire":  SPRITE_PU_RAPID_FIRE,
    "shield":      SPRITE_PU_SHIELD,
    "gun_upgrade": SPRITE_PU_DOUBLE_SHOT,
    "extra_life":  SPRITE_PU_EXTRA_LIFE,
    "rocket":      SPRITE_PU_ROCKET,
    "spread":      SPRITE_PU_DOUBLE_SHOT,
    "plasma":      SPRITE_PU_RAPID_FIRE,
    "laser":       SPRITE_PU_SHIELD,
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
