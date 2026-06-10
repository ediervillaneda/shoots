import pygame
from src.entities.rocket import Rocket
from src.settings import ROCKET_SPEED, ROCKET_W, ROCKET_H


def test_rocket_spawns_at_position():
    r = Rocket(270, 400)
    assert r.rect.centerx == 270
    assert r.rect.bottom == 400


def test_rocket_image_size():
    r = Rocket(270, 400)
    assert r.image.get_size() == (ROCKET_W, ROCKET_H)


def test_rocket_moves_up():
    r = Rocket(270, 400)
    initial_y = r.y
    r.update(1.0)
    assert r.y < initial_y


def test_rocket_speed():
    r = Rocket(270, 400)
    initial_y = r.y
    r.update(1.0)
    assert r.y == initial_y - ROCKET_SPEED


def test_rocket_killed_off_screen():
    r = Rocket(270, 0)
    group = pygame.sprite.Group(r)
    r.update(1.0)
    assert not r.alive()
