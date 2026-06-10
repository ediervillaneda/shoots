import pygame
import src.assets as assets
from src.settings import (
    PLAYER_SPEED,
    PLAYER_COLOR,
    PLAYER_W,
    PLAYER_H,
    SCREEN_W,
    SCREEN_H,
    BULLET_COOLDOWN,
    PLAYER_LIVES,
    PLAYER_LIVES_MAX,
    INVINCIBILITY_MS,
    RAPIDFIRE_COOLDOWN_MULT,
    SPRITE_SHIP,
    SPRITE_SHOT1,
    SPRITE_SHOT2,
    SPRITE_SHOT3,
    SPRITE_SHOT4,
    SPRITE_SHOT5,
    SPRITE_SHOT6,
    BULLET_W_L1,
    BULLET_H_L1,
    BULLET_W_L2,
    BULLET_H_L2,
    BULLET_W_L3,
    BULLET_H_L3,
    BULLET_W_L4,
    BULLET_H_L4,
    BULLET_W_L5,
    BULLET_H_L5,
    BULLET_W_L6,
    BULLET_H_L6,
    SHOT_LEVEL_MAX,
    ROCKET_COOLDOWN,
    ROCKET_ANGLE_DEG,
    ROCKET_MAX_COUNT,
)
from src.entities.bullet import Bullet
from src.entities.rocket import Rocket

SQRT2_INV = 0.7071067811865476  # 1/sqrt(2)


def calc_velocity(left, right, up, down):
    dx = float(right) - float(left)
    dy = float(down) - float(up)
    if dx != 0 and dy != 0:
        dx *= SQRT2_INV
        dy *= SQRT2_INV
    return dx, dy


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        raw = assets.get(SPRITE_SHIP)
        self.image = pygame.transform.scale(raw, (PLAYER_W, PLAYER_H))
        self.rect = self.image.get_rect(
            centerx=SCREEN_W // 2,
            bottom=SCREEN_H - 80,
        )
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.last_shot = -BULLET_COOLDOWN
        self.lives = PLAYER_LIVES
        self.invincible = False
        self.invincible_until = 0
        self.active_powerups: set[str] = set()
        self.shot_level: int = 1
        self.last_rocket: int = -ROCKET_COOLDOWN
        self.rocket_count: int = 0

    def apply_powerup(self, kind: str) -> None:
        if kind == "extra_life":
            self.lives = min(PLAYER_LIVES_MAX, self.lives + 1)
        elif kind == "gun_upgrade":
            self.shot_level = min(SHOT_LEVEL_MAX, self.shot_level + 1)
        elif kind == "rocket":
            self.rocket_count = min(ROCKET_MAX_COUNT, self.rocket_count + 1)
        else:
            self.active_powerups.add(kind)

    def take_damage(self, now: int) -> None:
        if self.invincible:
            return
        if "shield" in self.active_powerups:
            self.active_powerups.discard("shield")
            return
        self.lives = max(0, self.lives - 1)
        self.active_powerups.clear()
        self.shot_level = 1
        self.rocket_count = 0
        self.invincible = True
        self.invincible_until = now + INVINCIBILITY_MS

    def handle_keys(self, keys):
        self.vel_x, self.vel_y = calc_velocity(
            left=bool(keys[pygame.K_a]),
            right=bool(keys[pygame.K_d]),
            up=bool(keys[pygame.K_w]),
            down=bool(keys[pygame.K_s]),
        )

    def update(self, dt):
        self.x += self.vel_x * PLAYER_SPEED * dt
        self.y += self.vel_y * PLAYER_SPEED * dt
        self.x = max(0.0, min(float(SCREEN_W - PLAYER_W), self.x))
        self.y = max(0.0, min(float(SCREEN_H - PLAYER_H), self.y))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        now = pygame.time.get_ticks()
        if self.invincible and now >= self.invincible_until:
            self.invincible = False
            self.image.set_alpha(255)
        elif self.invincible:
            visible = (now // 100) % 2 == 0
            self.image.set_alpha(255 if visible else 0)

    def shoot(self, now: int) -> list[Bullet]:
        cooldown = BULLET_COOLDOWN
        if "rapid_fire" in self.active_powerups:
            cooldown = int(BULLET_COOLDOWN * RAPIDFIRE_COOLDOWN_MULT)
        if now - self.last_shot < cooldown:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        top = self.rect.top
        if self.shot_level >= 6:
            return [
                Bullet(cx - 28, top, SPRITE_SHOT6, BULLET_W_L6, BULLET_H_L6),
                Bullet(cx - 12, top, SPRITE_SHOT6, BULLET_W_L6, BULLET_H_L6),
                Bullet(cx,      top, SPRITE_SHOT6, BULLET_W_L6, BULLET_H_L6),
                Bullet(cx + 12, top, SPRITE_SHOT6, BULLET_W_L6, BULLET_H_L6),
                Bullet(cx + 28, top, SPRITE_SHOT6, BULLET_W_L6, BULLET_H_L6),
            ]
        if self.shot_level >= 5:
            return [
                Bullet(cx - 28, top, SPRITE_SHOT5, BULLET_W_L5, BULLET_H_L5),
                Bullet(cx - 12, top, SPRITE_SHOT5, BULLET_W_L5, BULLET_H_L5),
                Bullet(cx,      top, SPRITE_SHOT5, BULLET_W_L5, BULLET_H_L5),
                Bullet(cx + 12, top, SPRITE_SHOT5, BULLET_W_L5, BULLET_H_L5),
                Bullet(cx + 28, top, SPRITE_SHOT5, BULLET_W_L5, BULLET_H_L5),
            ]
        if self.shot_level >= 4:
            return [
                Bullet(cx - 16, top, SPRITE_SHOT4, BULLET_W_L4, BULLET_H_L4),
                Bullet(cx,      top, SPRITE_SHOT4, BULLET_W_L4, BULLET_H_L4),
                Bullet(cx + 16, top, SPRITE_SHOT4, BULLET_W_L4, BULLET_H_L4),
            ]
        if self.shot_level >= 3:
            return [
                Bullet(cx - 16, top, SPRITE_SHOT3, BULLET_W_L3, BULLET_H_L3),
                Bullet(cx,      top, SPRITE_SHOT3, BULLET_W_L3, BULLET_H_L3),
                Bullet(cx + 16, top, SPRITE_SHOT3, BULLET_W_L3, BULLET_H_L3),
            ]
        if self.shot_level >= 2:
            return [
                Bullet(cx - 10, top, SPRITE_SHOT2, BULLET_W_L2, BULLET_H_L2),
                Bullet(cx + 10, top, SPRITE_SHOT2, BULLET_W_L2, BULLET_H_L2),
            ]
        return [Bullet(cx, top, SPRITE_SHOT1, BULLET_W_L1, BULLET_H_L1)]

    def shoot_rocket(self, now: int) -> list[Rocket]:
        if self.rocket_count == 0:
            return []
        if now - self.last_rocket < ROCKET_COOLDOWN:
            return []
        self.last_rocket = now
        rockets = []
        if self.rocket_count >= 1:
            rockets.append(Rocket(self.rect.left, self.rect.top, -ROCKET_ANGLE_DEG))
        if self.rocket_count >= 2:
            rockets.append(Rocket(self.rect.right, self.rect.top, ROCKET_ANGLE_DEG))
        return rockets
