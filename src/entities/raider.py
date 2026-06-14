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
    ENEMY_FLASH_MS, ENEMY_FLASH_ALPHA,
)


class Raider(Enemy):
    def __init__(self):
        x = random.randint(RAIDER_W // 2, SCREEN_W - RAIDER_W // 2)
        super().__init__(x, RAIDER_W, RAIDER_H, RAIDER_COLOR, RAIDER_HP, RAIDER_POINTS)
        raw = assets.get(SPRITE_RAIDER)
        self.image = pygame.transform.scale(raw, (RAIDER_W, RAIDER_H))
        # NO flip vertical — entra desde abajo mirando hacia arriba (imagen ya orientada)
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
        top = self.rect.top  # dispara hacia arriba (hacia el player)
        return [
            EnemyBullet(cx, top, 180 - GUNNER_SPREAD_ANGLE, ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
            EnemyBullet(cx, top, 180,                        ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
            EnemyBullet(cx, top, 180 + GUNNER_SPREAD_ANGLE,  ENEMY_PROJ_VULCAN, ENEMY_PROJ_VULCAN_W, ENEMY_PROJ_VULCAN_H),
        ]

    def update(self, dt: float) -> None:
        speed = RAIDER_SPEED + getattr(self, "speed_bonus", 0.0)
        if self._state == "entering":
            self.y -= speed * dt  # sube
            if self.y <= RAIDER_PATROL_Y:
                self.y = float(RAIDER_PATROL_Y)
                self._state = "patrolling"
        elif self._state == "patrolling":
            self._patrol_timer += dt * 1000
            self.x += RAIDER_PATROL_SPEED * self._dir_x * dt
            if self.rect.right >= SCREEN_W:
                self._dir_x = -1.0
                self.rect.right = SCREEN_W
                self.x = float(self.rect.x)
            elif self.rect.left <= 0:
                self._dir_x = 1.0
                self.rect.left = 0
                self.x = float(self.rect.x)
            if self._patrol_timer >= RAIDER_PATROL_MS:
                self._state = "leaving"
        else:  # leaving
            self.y += speed * dt
            if self.rect.top >= SCREEN_H:
                self.kill()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        # Manejo de flash (sin llamar super().update porque empieza debajo de SCREEN_H)
        if self._flash_ms > 0 and self._base_image is not None:
            self._flash_ms -= dt * 1000
            flash = self._base_image.copy()
            flash.fill((255, 255, 255, ENEMY_FLASH_ALPHA), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = flash
        elif self._base_image is not None and self._flash_ms <= 0:
            self.image = self._base_image
            self._base_image = None
