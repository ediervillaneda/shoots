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
