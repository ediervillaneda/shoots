import pygame
import src.assets as assets
from src.settings import BULLET_SPEED, BULLET_W, BULLET_H, SPRITE_PLASMA


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path=SPRITE_PLASMA, w=BULLET_W, h=BULLET_H):
        super().__init__()
        raw = assets.get(sprite_path)
        self.image = pygame.transform.scale(raw, (w, h))
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.y = float(self.rect.y)

    def update(self, dt):
        self.y -= BULLET_SPEED * dt
        self.rect.y = int(self.y)
        if self.rect.bottom < 0:
            self.kill()
