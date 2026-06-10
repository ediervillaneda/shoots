import pygame
import src.assets as assets
from src.settings import BULLET_IMPACT_FRAME_MS


class ImpactEffect(pygame.sprite.Sprite):
    def __init__(self, cx: int, cy: int, frames: list[str], w: int, h: int):
        super().__init__()
        self._frames = [pygame.transform.scale(assets.get(p), (w, h)) for p in frames]
        self._idx = 0
        self._timer = 0.0
        self.image = self._frames[0]
        self.rect = self.image.get_rect(center=(cx, cy))

    def update(self, dt: float) -> None:
        self._timer += dt * 1000
        while self._timer >= BULLET_IMPACT_FRAME_MS:
            self._timer -= BULLET_IMPACT_FRAME_MS
            self._idx += 1
            if self._idx >= len(self._frames):
                self.kill()
                return
            self.image = self._frames[self._idx]
