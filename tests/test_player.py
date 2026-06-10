import math
import pygame
from src.entities.player import Player, calc_velocity
from src.settings import SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H, BULLET_COOLDOWN


def test_velocity_right():
    vx, vy = calc_velocity(left=False, right=True, up=False, down=False)
    assert vx == 1.0 and vy == 0.0

def test_velocity_left():
    vx, vy = calc_velocity(left=True, right=False, up=False, down=False)
    assert vx == -1.0 and vy == 0.0

def test_velocity_up():
    vx, vy = calc_velocity(left=False, right=False, up=True, down=False)
    assert vx == 0.0 and vy == -1.0

def test_velocity_diagonal_normalized():
    vx, vy = calc_velocity(left=False, right=True, up=True, down=False)
    magnitude = math.sqrt(vx**2 + vy**2)
    assert abs(magnitude - 1.0) < 0.001

def test_velocity_idle():
    vx, vy = calc_velocity(left=False, right=False, up=False, down=False)
    assert vx == 0.0 and vy == 0.0

def test_player_initial_position():
    player = Player()
    assert player.rect.centerx == SCREEN_W // 2
    assert player.rect.bottom == SCREEN_H - 80

def test_player_clamped_to_screen_right():
    player = Player()
    player.rect.x = SCREEN_W + 100
    player.x = float(player.rect.x)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.right <= SCREEN_W

def test_player_clamped_to_screen_left():
    player = Player()
    player.rect.x = -200
    player.x = float(player.rect.x)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.left >= 0

def test_player_shoot_returns_bullet():
    from src.entities.bullet import Bullet
    player = Player()
    player.last_shot = 0
    bullet = player.shoot(BULLET_COOLDOWN + 1)
    assert bullet is not None
    assert isinstance(bullet, Bullet)

def test_player_shoot_respects_cooldown():
    player = Player()
    player.last_shot = 1000
    bullet = player.shoot(1000 + BULLET_COOLDOWN - 1)
    assert bullet is None

def test_player_bullet_spawns_at_player_top():
    from src.entities.bullet import Bullet
    player = Player()
    player.last_shot = 0
    bullet = player.shoot(BULLET_COOLDOWN + 1)
    assert bullet.rect.centerx == player.rect.centerx
    assert bullet.rect.bottom == player.rect.top

def test_player_clamped_to_screen_bottom():
    player = Player()
    player.rect.y = SCREEN_H + 100
    player.y = float(player.rect.y)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.bottom <= SCREEN_H

def test_player_clamped_to_screen_top():
    player = Player()
    player.rect.y = -200
    player.y = float(player.rect.y)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.top >= 0
