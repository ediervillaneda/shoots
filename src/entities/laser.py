import pygame
from src.settings import SCREEN_H, LASER_W, LASER_COLOR, LASER_DURATION_MS, LASER_DAMAGE_PER_S


class Laser(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._elapsed_ms = 0.0
        self.image = pygame.Surface((LASER_W, SCREEN_H), pygame.SRCALPHA)
        self.image.fill((*LASER_COLOR, 180))
        self.rect = self.image.get_rect(
            centerx=player.rect.centerx,
            bottom=player.rect.top,
        )
        self.damage_per_s = LASER_DAMAGE_PER_S

    def update(self, dt: float) -> None:
        self._elapsed_ms += dt * 1000
        self.rect.centerx = self._player.rect.centerx
        self.rect.bottom = self._player.rect.top
        if self._elapsed_ms >= LASER_DURATION_MS:
            self.kill()
            self._player.active_powerups.discard("laser")
