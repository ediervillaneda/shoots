import pygame
from src.entities.scout import Scout
from src.settings import SCOUT_HP, SCOUT_POINTS, SCOUT_SPEED


def test_scout_hp():
    s = Scout(240)
    assert s.hp == SCOUT_HP


def test_scout_points():
    s = Scout(240)
    assert s.points == SCOUT_POINTS


def test_scout_moves_down():
    s = Scout(240)
    initial_y = s.y
    s.update(1.0)
    assert s.y == initial_y + SCOUT_SPEED


def test_scout_moves_straight_x():
    s = Scout(240)
    initial_x = s.rect.x
    s.update(1.0)
    assert s.rect.x == initial_x


def test_scout_killed_by_one_hit():
    s = Scout(240)
    group = pygame.sprite.Group(s)
    s.take_damage(1)
    assert not s.alive()


def test_scout_spawns_above_screen():
    s = Scout(240)
    assert s.rect.bottom == 0
