import math
import pytest
import pygame
from src.entities.enemy_bullet import EnemyBullet
from src.settings import ENEMY_BULLET_SPEED, SCREEN_H


def test_enemy_bullet_spawns_at_position():
    eb = EnemyBullet(270, 100)
    assert eb.rect.centerx == 270
    assert eb.rect.top == 100


def test_enemy_bullet_moves_down():
    eb = EnemyBullet(270, 100)
    initial_y = eb.y
    eb.update(1.0)
    assert eb.y > initial_y


def test_enemy_bullet_speed():
    eb = EnemyBullet(270, 100)
    initial_y = eb.y
    eb.update(1.0)
    assert eb.y == initial_y + ENEMY_BULLET_SPEED


def test_enemy_bullet_killed_off_screen():
    eb = EnemyBullet(270, SCREEN_H)
    group = pygame.sprite.Group(eb)
    eb.update(1.0)
    assert not eb.alive()


def test_enemy_bullet_zero_angle_no_horizontal_velocity():
    eb = EnemyBullet(270, 100, 0)
    assert eb._vx == pytest.approx(0.0, abs=1e-9)


def test_enemy_bullet_zero_angle_full_vertical_speed():
    eb = EnemyBullet(270, 100, 0)
    assert eb._vy == pytest.approx(ENEMY_BULLET_SPEED)


def test_enemy_bullet_positive_angle_moves_right():
    eb = EnemyBullet(270, 100, 20)
    assert eb._vx > 0


def test_enemy_bullet_negative_angle_moves_left():
    eb = EnemyBullet(270, 100, -20)
    assert eb._vx < 0


def test_enemy_bullet_diagonal_preserves_total_speed():
    eb = EnemyBullet(270, 100, 20)
    speed = math.hypot(eb._vx, eb._vy)
    assert speed == pytest.approx(ENEMY_BULLET_SPEED)


def test_enemy_bullet_diagonal_moves_horizontally():
    eb = EnemyBullet(270, 100, 20)
    initial_x = eb.x
    eb.update(1.0)
    assert eb.x > initial_x
