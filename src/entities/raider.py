import random
import pygame
import src.assets as assets
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    RAIDER_SPEED, RAIDER_COLOR, RAIDER_W, RAIDER_H,
    RAIDER_HP, RAIDER_POINTS,
    RAIDER_PATROL_Y, RAIDER_PATROL_SPEED, RAIDER_PATROL_MS,
    SCREEN_W, SCREEN_H, SPRITE_RAIDER,
    GUNNER_SHOOT_INTERVAL, GUNNER_SPREAD_ANGLE,
    ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H,
)


class Raider(Enemy):
    def __init__(self):
        x = random.randint(RAIDER_W // 2, SCREEN_W - RAIDER_W // 2)
        super().__init__(x, RAIDER_W, RAIDER_H, RAIDER_COLOR, RAIDER_HP, RAIDER_POINTS)
        raw = assets.get(SPRITE_RAIDER)
        self.image = pygame.transform.scale(raw, (RAIDER_W, RAIDER_H))
        self.rect = self.image.get_rect(centerx=x, top=SCREEN_H)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self._state = "entering"
        self._patrol_timer = 0.0
        self._dir_x = 1.0 if x < SCREEN_W // 2 else -1.0
        self.last_shot: int = -GUNNER_SHOOT_INTERVAL

    def shoot(self, now: int) -> list:
        if self._state != "patrolling":
            return []
        if now - self.last_shot < GUNNER_SHOOT_INTERVAL:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        top = self.rect.top
        return [
            EnemyBullet(cx, top, 180 - GUNNER_SPREAD_ANGLE, ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
            EnemyBullet(cx, top, 180,                        ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
            EnemyBullet(cx, top, 180 + GUNNER_SPREAD_ANGLE,  ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
        ]

    def update(self, dt: float) -> None:
        speed = RAIDER_SPEED + getattr(self, "speed_bonus", 0.0)
        if self._state == "entering":
            self.y -= speed * dt
            if self.y <= RAIDER_PATROL_Y:
                self.y = float(RAIDER_PATROL_Y)
                self._state = "patrolling"
        elif self._state == "patrolling":
            self._patrol_timer += dt * 1000
            self.x += RAIDER_PATROL_SPEED * self._dir_x * dt
            # fix: usar self.x directamente para evitar rect desactualizado
            if self.x + RAIDER_W >= SCREEN_W:
                self._dir_x = -1.0
                self.x = float(SCREEN_W - RAIDER_W)
            elif self.x <= 0:
                self._dir_x = 1.0
                self.x = 0.0
            if self._patrol_timer >= RAIDER_PATROL_MS:
                self._state = "leaving"
        else:  # leaving
            self.y += speed * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        # rect.top = SCREEN_H (no >) al inicio: super().update() no mata prematuramente
        super().update(dt)  # flash + kill cuando rect.top > SCREEN_H
