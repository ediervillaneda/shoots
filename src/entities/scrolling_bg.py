import pygame
import src.assets as assets
from src.settings import SCREEN_W, SCREEN_H, BG_SCROLL_SPEED, SPRITE_BG


class ScrollingBG:
    def __init__(self):
        raw = assets.get(SPRITE_BG)
        scale_h = max(SCREEN_H, int(raw.get_height() * SCREEN_W / raw.get_width()))
        self._tile = pygame.transform.scale(raw, (SCREEN_W, scale_h))
        self._h = scale_h
        self._y1 = 0.0
        self._y2 = float(-scale_h)

    def update(self, dt: float) -> None:
        self._y1 += BG_SCROLL_SPEED * dt
        self._y2 += BG_SCROLL_SPEED * dt
        if self._y1 >= SCREEN_H:
            self._y1 = self._y2 - self._h
        if self._y2 >= SCREEN_H:
            self._y2 = self._y1 - self._h

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._tile, (0, int(self._y1)))
        screen.blit(self._tile, (0, int(self._y2)))
