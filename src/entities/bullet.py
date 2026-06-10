import pygame
import src.assets as assets
from src.settings import (
    BULLET_SPEED, BULLET_W_L1, BULLET_H_L1,
    SHOT1_LAUNCH_FRAMES, SHOT1_TRAVEL, SHOT1_IMPACT_FRAMES,
    BULLET_LAUNCH_FRAME_MS,
)


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        launch_frames: list[str] | None = None,
        travel_path: str | None = None,
        impact_frames: list[str] | None = None,
        w: int = BULLET_W_L1,
        h: int = BULLET_H_L1,
    ):
        super().__init__()
        if launch_frames is None:
            launch_frames = SHOT1_LAUNCH_FRAMES
        if travel_path is None:
            travel_path = SHOT1_TRAVEL
        if impact_frames is None:
            impact_frames = SHOT1_IMPACT_FRAMES

        self.w = w
        self.h = h
        self.impact_frames = impact_frames

        self._launch_imgs = [
            pygame.transform.scale(assets.get(p), (w, h)) for p in launch_frames
        ]
        self._travel_img = pygame.transform.scale(assets.get(travel_path), (w, h))
        self._frame_idx = 0
        self._frame_timer = 0.0
        self._launching = True

        self.image = self._launch_imgs[0]
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.y = float(self.rect.y)

    def update(self, dt: float) -> None:
        if self._launching:
            self._frame_timer += dt * 1000
            if self._frame_timer >= BULLET_LAUNCH_FRAME_MS:
                self._frame_timer -= BULLET_LAUNCH_FRAME_MS
                self._frame_idx += 1
                if self._frame_idx >= len(self._launch_imgs):
                    self._launching = False
                    self.image = self._travel_img
                else:
                    self.image = self._launch_imgs[self._frame_idx]

        self.y -= BULLET_SPEED * dt
        self.rect.y = int(self.y)
        if self.rect.bottom < 0:
            self.kill()
