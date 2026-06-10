import math
import pytest
import pygame
from src.entities.kamikaze import Kamikaze
from src.settings import KAMIKAZE_SPEED, KAMIKAZE_HP, KAMIKAZE_POINTS, KAMIKAZE_W, KAMIKAZE_H


def test_kamikaze_hp():
    k = Kamikaze(240)
    assert k.hp == KAMIKAZE_HP


def test_kamikaze_points():
    k = Kamikaze(240)
    assert k.points == KAMIKAZE_POINTS


def test_kamikaze_spawns_above_screen():
    k = Kamikaze(240)
    assert k.rect.bottom == 0


def test_kamikaze_image_size():
    k = Kamikaze(240)
    assert k.image.get_size() == (KAMIKAZE_W, KAMIKAZE_H)


def test_kamikaze_falls_straight_without_target():
    k = Kamikaze(240)
    initial_y = k.y
    k.update(1.0)
    assert k.y > initial_y


def test_kamikaze_uses_speed_bonus():
    k = Kamikaze(240)
    k.speed_bonus = 50.0
    initial_y = k.y
    k.update(1.0)
    assert k.y == pytest.approx(initial_y + KAMIKAZE_SPEED + 50.0)


def test_kamikaze_tracks_target_horizontally():
    k = Kamikaze(100)  # rect.centerx == 100
    class FakePlayer:
        rect = pygame.Rect(400, 300, 40, 50)  # centerx == 420
    k.target = FakePlayer()
    k.update(1.0)
    assert k.rect.centerx > 100


def test_kamikaze_take_damage_reduces_hp():
    k = Kamikaze(240)
    k.take_damage(1)
    assert k.hp == KAMIKAZE_HP - 1


def test_kamikaze_dies_at_zero_hp():
    k = Kamikaze(240)
    group = pygame.sprite.Group(k)
    for _ in range(KAMIKAZE_HP):
        k.take_damage(1)
    assert not k.alive()
