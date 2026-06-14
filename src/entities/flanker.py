import random
import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.settings import (
    FLANKER_SPEED, FLANKER_COLOR, FLANKER_W, FLANKER_H,
    FLANKER_HP, FLANKER_POINTS, FLANKER_CROSS_Y,
    SCREEN_W, SCREEN_H, SPRITE_FLANKER,
)


class Flanker(Enemy):
    def __init__(self, from_left: bool):
        # x placeholder para Enemy.__init__; se reposiciona después
        super().__init__(0, FLANKER_W, FLANKER_H, FLANKER_COLOR, FLANKER_HP, FLANKER_POINTS)
        raw = assets.get(SPRITE_FLANKER)
        self.image = pygame.transform.scale(raw, (FLANKER_W, FLANKER_H))
        self.image = pygame.transform.flip(self.image, False, True)
        # posicionar en el lateral con y en FLANKER_CROSS_Y
        if from_left:
            self.rect = self.image.get_rect(right=0, centery=FLANKER_CROSS_Y)
        else:
            self.rect = self.image.get_rect(left=SCREEN_W, centery=FLANKER_CROSS_Y)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self._from_left = from_left
        self._state = "crossing"
        self._target_x = float(random.randint(SCREEN_W // 4, SCREEN_W * 3 // 4))

    def update(self, dt: float) -> None:
        speed = FLANKER_SPEED + getattr(self, "speed_bonus", 0.0)
        if self._state == "crossing":
            if self._from_left:
                self.x += speed * dt
                if self.x + FLANKER_W // 2 >= self._target_x:
                    self.x = self._target_x - FLANKER_W // 2
                    self._state = "descending"
            else:
                self.x -= speed * dt
                if self.x + FLANKER_W // 2 <= self._target_x:
                    self.x = self._target_x - FLANKER_W // 2
                    self._state = "descending"
        else:  # descending
            self.y += speed * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        super().update(dt)  # flash + kill check cuando sale por abajo
