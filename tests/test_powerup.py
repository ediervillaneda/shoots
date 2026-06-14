import pytest
import pygame
from src.entities.powerup import PowerUp, POWERUP_KINDS, POWERUP_ASSETS
from src.settings import POWERUP_SPEED, POWERUP_W, POWERUP_H, SCREEN_H


def test_powerup_has_kind():
    pu = PowerUp("shield", 270, 100)
    assert pu.kind == "shield"


def test_powerup_spawns_at_position():
    pu = PowerUp("rapid_fire", 270, 100)
    assert pu.rect.centerx == 270
    assert pu.rect.top == 100


def test_powerup_image_size():
    pu = PowerUp("shield", 270, 100)
    assert pu.image.get_size() == (POWERUP_W, POWERUP_H)


def test_powerup_moves_down():
    pu = PowerUp("shield", 270, 100)
    initial_y = pu.y
    pu.update(1.0)
    assert pu.y > initial_y


def test_powerup_speed():
    pu = PowerUp("shield", 270, 100)
    initial_y = pu.y
    pu.update(1.0)
    assert pu.y == pytest.approx(initial_y + POWERUP_SPEED)


def test_powerup_killed_off_screen():
    pu = PowerUp("gun_upgrade", 270, SCREEN_H)
    group = pygame.sprite.Group(pu)
    pu.update(1.0)
    assert not pu.alive()


def test_powerup_kinds_contains_all_kinds():
    assert set(POWERUP_KINDS) == {
        "rapid_fire", "shield", "gun_upgrade", "extra_life", "rocket",
        "spread", "plasma", "laser",
    }


def test_powerup_assets_keys_match_kinds():
    assert set(POWERUP_ASSETS.keys()) == set(POWERUP_KINDS)


def test_all_kind_strings_valid():
    for kind in POWERUP_KINDS:
        pu = PowerUp(kind, 270, 100)
        assert pu.kind == kind
