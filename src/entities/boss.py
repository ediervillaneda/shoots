import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    SCREEN_W,
    BOSS_W, BOSS_H, BOSS_HP, BOSS_POINTS, BOSS_SPEED, BOSS_COLOR,
    BOSS_Y_TARGET, BOSS_SHOOT_INTERVAL_P1, BOSS_SHOOT_INTERVAL_P2,
    BOSS_SPREAD_ANGLE,
)


class Boss(Enemy):
    def __init__(self, sprite_path: str):
        super().__init__(SCREEN_W // 2, BOSS_W, BOSS_H, BOSS_COLOR, BOSS_HP, BOSS_POINTS)
        raw = assets.get(sprite_path)
        self.image = pygame.transform.scale(raw, (BOSS_W, BOSS_H))
        self.rect = self.image.get_rect(centerx=SCREEN_W // 2, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.phase: int = 1
        self.dir: int = 1
        self.last_shot: int = -BOSS_SHOOT_INTERVAL_P1
        self._entry_done: bool = False

    def shoot(self, now: int) -> list[EnemyBullet]:
        interval = BOSS_SHOOT_INTERVAL_P1 if self.phase == 1 else BOSS_SHOOT_INTERVAL_P2
        if now - self.last_shot < interval:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        bottom = self.rect.bottom
        if self.phase == 1:
            return [EnemyBullet(cx, bottom)]
        return [
            EnemyBullet(cx, bottom, -BOSS_SPREAD_ANGLE),
            EnemyBullet(cx, bottom, 0),
            EnemyBullet(cx, bottom, +BOSS_SPREAD_ANGLE),
        ]

    def update(self, dt: float) -> None:
        if not self._entry_done:
            self.y += BOSS_SPEED * dt
            if self.y >= BOSS_Y_TARGET:
                self._entry_done = True
        else:
            self.x += BOSS_SPEED * self.dir * dt
        self.phase = 1 if self.hp > BOSS_HP // 2 else 2
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self._entry_done:
            if self.rect.right >= SCREEN_W:
                self.dir = -1
                self.rect.right = SCREEN_W
                self.x = float(self.rect.x)
            elif self.rect.left <= 0:
                self.dir = 1
                self.rect.left = 0
                self.x = float(self.rect.x)
        # Do NOT call super().update(dt) — Enemy.update() kills sprites when
        # they exit SCREEN_H bottom. Boss starts off-screen top and descends,
        # so calling super would kill it immediately.
