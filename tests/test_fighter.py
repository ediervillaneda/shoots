import math
import pygame
from src.entities.fighter import Fighter
from src.settings import (
    FIGHTER_HP, FIGHTER_POINTS, FIGHTER_SPEED,
    FIGHTER_AMPLITUDE, FIGHTER_FREQUENCY,
)


def test_fighter_hp():
    f = Fighter(240)
    assert f.hp == FIGHTER_HP


def test_fighter_points():
    f = Fighter(240)
    assert f.points == FIGHTER_POINTS


def test_fighter_moves_down():
    f = Fighter(240)
    initial_y = f.y
    f.update(1.0)
    assert f.y > initial_y


def test_fighter_down_speed():
    f = Fighter(240)
    initial_y = f.y
    f.update(1.0)
    assert f.y == initial_y + FIGHTER_SPEED


def test_fighter_oscillates_horizontally():
    f = Fighter(240)
    quarter_period = 1.0 / (FIGHTER_FREQUENCY * 4)
    f.update(quarter_period)
    expected_x = int(f.origin_x + math.sin(quarter_period * FIGHTER_FREQUENCY * 2 * math.pi) * FIGHTER_AMPLITUDE)
    assert f.rect.x == expected_x


def test_fighter_survives_two_hits():
    f = Fighter(240)
    group = pygame.sprite.Group(f)
    f.take_damage(1)
    f.take_damage(1)
    assert f.alive()
    assert f.hp == 1


def test_fighter_killed_by_three_hits():
    f = Fighter(240)
    group = pygame.sprite.Group(f)
    f.take_damage(1)
    f.take_damage(1)
    f.take_damage(1)
    assert not f.alive()


def test_fighter_spawns_above_screen():
    f = Fighter(240)
    assert f.rect.bottom == 0
