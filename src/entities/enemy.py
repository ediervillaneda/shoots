import pygame
from src.settings import SCREEN_H, ENEMY_FLASH_MS


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, w, h, color, hp, points):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self._base_image = self.image.copy()
        self.rect = self.image.get_rect(centerx=x, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.hp = hp
        self.points = points
        self._flash_ms = 0.0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
        else:
            self._flash_ms = float(ENEMY_FLASH_MS)

    def update(self, dt):
        if self._flash_ms > 0:
            self._flash_ms -= dt * 1000
            flash = self._base_image.copy()
            flash.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = flash
        else:
            self.image = self._base_image
        if self.rect.top > SCREEN_H:
            self.kill()
