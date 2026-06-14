import pygame
import src.assets as assets
from src.settings import (
    PLAYER_SPEED,
    PLAYER_COLOR,
    PLAYER_W,
    PLAYER_H,
    PLAYER_BANK_LERP,
    PLAYER_SHADOW_OFFSET_X,
    PLAYER_SHADOW_OFFSET_Y,
    SCREEN_W,
    SCREEN_H,
    BULLET_COOLDOWN,
    PLAYER_LIVES,
    PLAYER_LIVES_MAX,
    INVINCIBILITY_MS,
    RAPIDFIRE_COOLDOWN_MULT,
    SPRITE_PLAYER_L2, SPRITE_PLAYER_L1, SPRITE_PLAYER_M, SPRITE_PLAYER_R1, SPRITE_PLAYER_R2,
    SPRITE_PLAYER_SHADOW_L2, SPRITE_PLAYER_SHADOW_L1, SPRITE_PLAYER_SHADOW_M,
    SPRITE_PLAYER_SHADOW_R1, SPRITE_PLAYER_SHADOW_R2,
    SHOT1_LAUNCH_FRAMES, SHOT1_TRAVEL, SHOT1_IMPACT_FRAMES,
    SHOT2_LAUNCH_FRAMES, SHOT2_TRAVEL, SHOT2_IMPACT_FRAMES,
    SHOT3_LAUNCH_FRAMES, SHOT3_TRAVEL, SHOT3_IMPACT_FRAMES,
    SHOT4_LAUNCH_FRAMES, SHOT4_TRAVEL, SHOT4_IMPACT_FRAMES,
    SHOT5_LAUNCH_FRAMES, SHOT5_TRAVEL, SHOT5_IMPACT_FRAMES,
    SHOT6_LAUNCH_FRAMES, SHOT6_TRAVEL, SHOT6_IMPACT_FRAMES,
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
    BULLET_DAMAGE_DEFAULT,
    BULLET_TINT_RAPIDFIRE,
    BULLET_TINT_SHIELD,
    GUN_UPGRADE_DIVERGE_DEG,
    SPREAD_ANGLES, SPREAD_DAMAGE,
    PLASMA_SPEED_MULT, PLASMA_DAMAGE, PLASMA_TINT,
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


_POSE_KEYS = ('l2', 'l1', 'm', 'r1', 'r2')
_POSE_THRESHOLDS = (-0.6, -0.2, 0.2, 0.6)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._sprites = {
            'l2': pygame.transform.scale(assets.get(SPRITE_PLAYER_L2), (PLAYER_W, PLAYER_H)),
            'l1': pygame.transform.scale(assets.get(SPRITE_PLAYER_L1), (PLAYER_W, PLAYER_H)),
            'm':  pygame.transform.scale(assets.get(SPRITE_PLAYER_M),  (PLAYER_W, PLAYER_H)),
            'r1': pygame.transform.scale(assets.get(SPRITE_PLAYER_R1), (PLAYER_W, PLAYER_H)),
            'r2': pygame.transform.scale(assets.get(SPRITE_PLAYER_R2), (PLAYER_W, PLAYER_H)),
        }
        self._shadows = {
            'l2': pygame.transform.scale(assets.get(SPRITE_PLAYER_SHADOW_L2), (PLAYER_W, PLAYER_H)),
            'l1': pygame.transform.scale(assets.get(SPRITE_PLAYER_SHADOW_L1), (PLAYER_W, PLAYER_H)),
            'm':  pygame.transform.scale(assets.get(SPRITE_PLAYER_SHADOW_M),  (PLAYER_W, PLAYER_H)),
            'r1': pygame.transform.scale(assets.get(SPRITE_PLAYER_SHADOW_R1), (PLAYER_W, PLAYER_H)),
            'r2': pygame.transform.scale(assets.get(SPRITE_PLAYER_SHADOW_R2), (PLAYER_W, PLAYER_H)),
        }
        self._bank = 0.0
        self.image = self._sprites['m']
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

    def _pose_key(self) -> str:
        b = self._bank
        if b < _POSE_THRESHOLDS[0]:
            return 'l2'
        if b < _POSE_THRESHOLDS[1]:
            return 'l1'
        if b > _POSE_THRESHOLDS[3]:
            return 'r2'
        if b > _POSE_THRESHOLDS[2]:
            return 'r1'
        return 'm'

    @property
    def shadow_image(self) -> pygame.Surface:
        return self._shadows[self._pose_key()]

    @property
    def shadow_rect(self) -> pygame.Rect:
        return self.shadow_image.get_rect(
            centerx=self.rect.centerx + PLAYER_SHADOW_OFFSET_X,
            centery=self.rect.centery + PLAYER_SHADOW_OFFSET_Y,
        )

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
            left=bool(keys[pygame.K_a]) or bool(keys[pygame.K_LEFT]),
            right=bool(keys[pygame.K_d]) or bool(keys[pygame.K_RIGHT]),
            up=bool(keys[pygame.K_w]) or bool(keys[pygame.K_UP]),
            down=bool(keys[pygame.K_s]) or bool(keys[pygame.K_DOWN]),
        )

    def update(self, dt):
        self._bank += (self.vel_x - self._bank) * PLAYER_BANK_LERP * dt
        self._bank = max(-1.0, min(1.0, self._bank))

        self.x += self.vel_x * PLAYER_SPEED * dt
        self.y += self.vel_y * PLAYER_SPEED * dt
        self.x = max(0.0, min(float(SCREEN_W - PLAYER_W), self.x))
        self.y = max(0.0, min(float(SCREEN_H - PLAYER_H), self.y))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.image = self._sprites[self._pose_key()]

        now = pygame.time.get_ticks()
        if self.invincible:
            if now >= self.invincible_until:
                self.invincible = False
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(255 if (now // 100) % 2 == 0 else 0)
        else:
            self.image.set_alpha(255)

    def shoot(self, now: int) -> list[Bullet]:
        cooldown = BULLET_COOLDOWN
        if "rapid_fire" in self.active_powerups:
            cooldown = int(BULLET_COOLDOWN * RAPIDFIRE_COOLDOWN_MULT)
        if now - self.last_shot < cooldown:
            return []
        self.last_shot = now
        cx = self.rect.centerx
        top = self.rect.top
        damage = BULLET_DAMAGE_DEFAULT
        tint = None
        if "rapid_fire" in self.active_powerups:
            damage = max(1, int(BULLET_DAMAGE_DEFAULT * 0.5))
            tint = BULLET_TINT_RAPIDFIRE
        if "shield" in self.active_powerups:
            tint = BULLET_TINT_SHIELD
        # spread: 5 balas en abanico — tiene precedencia sobre gun_upgrade
        if "spread" in self.active_powerups:
            return [
                Bullet(cx, top, SHOT2_LAUNCH_FRAMES, SHOT2_TRAVEL, SHOT2_IMPACT_FRAMES,
                       BULLET_W_L2, BULLET_H_L2,
                       angle_deg=a, damage=SPREAD_DAMAGE, tint=tint)
                for a in SPREAD_ANGLES
            ]

        # plasma: 1 bala Shot6 lenta, daño alto
        if "plasma" in self.active_powerups:
            return [
                Bullet(cx, top, SHOT6_LAUNCH_FRAMES, SHOT6_TRAVEL, SHOT6_IMPACT_FRAMES,
                       BULLET_W_L6, BULLET_H_L6,
                       speed_mult=PLASMA_SPEED_MULT, damage=PLASMA_DAMAGE, tint=PLASMA_TINT)
            ]

        if self.shot_level >= 6:
            d = GUN_UPGRADE_DIVERGE_DEG
            return [
                Bullet(cx - 28, top, SHOT6_LAUNCH_FRAMES, SHOT6_TRAVEL, SHOT6_IMPACT_FRAMES, BULLET_W_L6, BULLET_H_L6, angle_deg=-2*d, damage=damage, tint=tint),
                Bullet(cx - 12, top, SHOT6_LAUNCH_FRAMES, SHOT6_TRAVEL, SHOT6_IMPACT_FRAMES, BULLET_W_L6, BULLET_H_L6, angle_deg=-d,   damage=damage, tint=tint),
                Bullet(cx,      top, SHOT6_LAUNCH_FRAMES, SHOT6_TRAVEL, SHOT6_IMPACT_FRAMES, BULLET_W_L6, BULLET_H_L6, angle_deg=0.0,  damage=damage, tint=tint),
                Bullet(cx + 12, top, SHOT6_LAUNCH_FRAMES, SHOT6_TRAVEL, SHOT6_IMPACT_FRAMES, BULLET_W_L6, BULLET_H_L6, angle_deg=+d,   damage=damage, tint=tint),
                Bullet(cx + 28, top, SHOT6_LAUNCH_FRAMES, SHOT6_TRAVEL, SHOT6_IMPACT_FRAMES, BULLET_W_L6, BULLET_H_L6, angle_deg=+2*d, damage=damage, tint=tint),
            ]
        if self.shot_level >= 5:
            d = GUN_UPGRADE_DIVERGE_DEG
            return [
                Bullet(cx - 28, top, SHOT5_LAUNCH_FRAMES, SHOT5_TRAVEL, SHOT5_IMPACT_FRAMES, BULLET_W_L5, BULLET_H_L5, angle_deg=-2*d, damage=damage, tint=tint),
                Bullet(cx - 12, top, SHOT5_LAUNCH_FRAMES, SHOT5_TRAVEL, SHOT5_IMPACT_FRAMES, BULLET_W_L5, BULLET_H_L5, angle_deg=-d,   damage=damage, tint=tint),
                Bullet(cx,      top, SHOT5_LAUNCH_FRAMES, SHOT5_TRAVEL, SHOT5_IMPACT_FRAMES, BULLET_W_L5, BULLET_H_L5, angle_deg=0.0,  damage=damage, tint=tint),
                Bullet(cx + 12, top, SHOT5_LAUNCH_FRAMES, SHOT5_TRAVEL, SHOT5_IMPACT_FRAMES, BULLET_W_L5, BULLET_H_L5, angle_deg=+d,   damage=damage, tint=tint),
                Bullet(cx + 28, top, SHOT5_LAUNCH_FRAMES, SHOT5_TRAVEL, SHOT5_IMPACT_FRAMES, BULLET_W_L5, BULLET_H_L5, angle_deg=+2*d, damage=damage, tint=tint),
            ]
        if self.shot_level >= 4:
            d = GUN_UPGRADE_DIVERGE_DEG
            return [
                Bullet(cx - 16, top, SHOT4_LAUNCH_FRAMES, SHOT4_TRAVEL, SHOT4_IMPACT_FRAMES, BULLET_W_L4, BULLET_H_L4, angle_deg=-d,  damage=damage, tint=tint),
                Bullet(cx,      top, SHOT4_LAUNCH_FRAMES, SHOT4_TRAVEL, SHOT4_IMPACT_FRAMES, BULLET_W_L4, BULLET_H_L4, angle_deg=0.0, damage=damage, tint=tint),
                Bullet(cx + 16, top, SHOT4_LAUNCH_FRAMES, SHOT4_TRAVEL, SHOT4_IMPACT_FRAMES, BULLET_W_L4, BULLET_H_L4, angle_deg=+d,  damage=damage, tint=tint),
            ]
        if self.shot_level >= 3:
            d = GUN_UPGRADE_DIVERGE_DEG
            return [
                Bullet(cx - 16, top, SHOT3_LAUNCH_FRAMES, SHOT3_TRAVEL, SHOT3_IMPACT_FRAMES, BULLET_W_L3, BULLET_H_L3, angle_deg=-d,  damage=damage, tint=tint),
                Bullet(cx,      top, SHOT3_LAUNCH_FRAMES, SHOT3_TRAVEL, SHOT3_IMPACT_FRAMES, BULLET_W_L3, BULLET_H_L3, angle_deg=0.0, damage=damage, tint=tint),
                Bullet(cx + 16, top, SHOT3_LAUNCH_FRAMES, SHOT3_TRAVEL, SHOT3_IMPACT_FRAMES, BULLET_W_L3, BULLET_H_L3, angle_deg=+d,  damage=damage, tint=tint),
            ]
        if self.shot_level >= 2:
            d = GUN_UPGRADE_DIVERGE_DEG * 0.5
            return [
                Bullet(cx - 10, top, SHOT2_LAUNCH_FRAMES, SHOT2_TRAVEL, SHOT2_IMPACT_FRAMES, BULLET_W_L2, BULLET_H_L2, angle_deg=-d, damage=damage, tint=tint),
                Bullet(cx + 10, top, SHOT2_LAUNCH_FRAMES, SHOT2_TRAVEL, SHOT2_IMPACT_FRAMES, BULLET_W_L2, BULLET_H_L2, angle_deg=+d, damage=damage, tint=tint),
            ]
        return [Bullet(cx, top, SHOT1_LAUNCH_FRAMES, SHOT1_TRAVEL, SHOT1_IMPACT_FRAMES, BULLET_W_L1, BULLET_H_L1, damage=damage, tint=tint)]

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
