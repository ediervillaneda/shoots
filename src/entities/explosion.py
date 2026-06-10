import pygame
import src.assets as assets
from src.settings import EXPLOSION_W, EXPLOSION_H, EXPLOSION_FRAME_MS, EXPLOSION_FRAMES


class Explosion(pygame.sprite.Sprite):
    def __init__(
        self,
        cx: int,
        cy: int,
        paths: list[str] | None = None,
        size: tuple[int, int] | None = None,
    ):
        super().__init__()
        if paths is None:
            paths = EXPLOSION_FRAMES
        if size is None:
            size = (EXPLOSION_W, EXPLOSION_H)
        self._frames = [pygame.transform.scale(assets.get(p), size) for p in paths]
        self._frame = 0
        self._elapsed = 0.0
        self.image = self._frames[0]
        self.rect = self.image.get_rect(center=(cx, cy))

    def update(self, dt: float) -> None:
        self._elapsed += dt * 1000
        while self._elapsed >= EXPLOSION_FRAME_MS:
            self._elapsed -= EXPLOSION_FRAME_MS
            self._frame += 1
            if self._frame >= len(self._frames):
                self.kill()
                return
            self.image = self._frames[self._frame]
