import pygame
from src.settings import (
    PLAYER_SPEED, PLAYER_COLOR, PLAYER_W, PLAYER_H,
    SCREEN_W, SCREEN_H, BULLET_COOLDOWN,
    PLAYER_LIVES, PLAYER_LIVES_MAX, INVINCIBILITY_MS, RAPIDFIRE_COOLDOWN_MULT,
)
from src.entities.bullet import Bullet

SQRT2_INV = 0.7071067811865476  # 1/sqrt(2)


def calc_velocity(left, right, up, down):
    """Calcula vector de velocidad normalizado a partir de teclas booleanas."""
    dx = float(right) - float(left)
    dy = float(down) - float(up)
    if dx != 0 and dy != 0:
        dx *= SQRT2_INV
        dy *= SQRT2_INV
    return dx, dy


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_W, PLAYER_H))
        self.image.fill(PLAYER_COLOR)
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

    def apply_powerup(self, kind: str) -> None:
        if kind == "extra_life":
            self.lives = min(PLAYER_LIVES_MAX, self.lives + 1)
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

    def shoot(self, now: int) -> list:
        cooldown = BULLET_COOLDOWN
        if "rapid_fire" in self.active_powerups:
            cooldown = int(BULLET_COOLDOWN * RAPIDFIRE_COOLDOWN_MULT)
        if now - self.last_shot < cooldown:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        top = self.rect.top
        if "triple_shot" in self.active_powerups:
            return [Bullet(cx, top), Bullet(cx - 16, top), Bullet(cx + 16, top)]
        if "double_shot" in self.active_powerups:
            return [Bullet(cx - 10, top), Bullet(cx + 10, top)]
        return [Bullet(cx, top)]
