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
