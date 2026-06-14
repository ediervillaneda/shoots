import pygame
from src.entities.bullet import Bullet
from src.settings import BULLET_SPEED, BULLET_H

def test_bullet_moves_up():
    bullet = Bullet(240, 400)
    initial_y = bullet.y
    bullet.update(1.0)
    assert bullet.y == initial_y - BULLET_SPEED

def test_bullet_stays_alive_mid_screen():
    bullet = Bullet(240, 400)
    group = pygame.sprite.Group(bullet)
    bullet.update(0.016)
    assert bullet.alive()

def test_bullet_killed_when_off_screen():
    bullet = Bullet(240, BULLET_H)  # rect.top = 0
    group = pygame.sprite.Group(bullet)
    bullet.update(1.0)              # sube 720px — fuera de pantalla
    assert not bullet.alive()

def test_bullet_rect_x_matches_spawn():
    bullet = Bullet(100, 300)
    assert bullet.rect.centerx == 100


def test_bullet_default_moves_straight_up():
    b = Bullet(270, 500)
    b.update(1.0)
    assert b.rect.y < 500


def test_bullet_angle_moves_right_when_positive():
    b = Bullet(270, 500, angle_deg=30.0)
    b.update(1.0)
    assert b.rect.x > 270 - b.w // 2


def test_bullet_damage_default():
    b = Bullet(270, 500)
    assert b.damage == 1


def test_bullet_custom_damage():
    b = Bullet(270, 500, damage=5)
    assert b.damage == 5


def test_bullet_tint_does_not_crash():
    b = Bullet(270, 500, tint=(80, 160, 255, 255))
    assert b.image is not None


def test_bullet_speed_mult_zero_stays_put():
    b = Bullet(270, 500, speed_mult=0.0)
    orig_x = b.rect.x
    orig_y = b.rect.y
    b.update(1.0)
    assert b.rect.x == orig_x
    assert b.rect.y == orig_y
