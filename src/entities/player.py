import pygame
from src.settings import (
    PLAYER_SPEED, PLAYER_COLOR, PLAYER_W, PLAYER_H,
    SCREEN_W, SCREEN_H, BULLET_COOLDOWN,
    PLAYER_LIVES, INVINCIBILITY_MS,
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
        self.last_shot = 0
        self.lives = PLAYER_LIVES
        self.invincible = False
        self.invincible_until = 0

    def take_damage(self, now):
        if self.invincible:
            return
        self.lives -= 1
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

    def shoot(self, now):
        if now - self.last_shot >= BULLET_COOLDOWN:
            self.last_shot = now
            return Bullet(self.rect.centerx, self.rect.top)
        return None
