import pygame
import pytest
from src.entities.gunner import Gunner
from src.entities.striker import Striker
from src.entities.interceptor import Interceptor
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    GUNNER_HP, GUNNER_POINTS, GUNNER_SHOOT_INTERVAL,
    STRIKER_HP, STRIKER_POINTS, STRIKER_SHOOT_INTERVAL, STRIKER_ENTRY_Y,
    INTERCEPTOR_HP, INTERCEPTOR_POINTS, INTERCEPTOR_SHOOT_INTERVAL,
    INTERCEPTOR_Y_TARGET, SCREEN_W,
)


# --- Gunner ---

def test_gunner_initial_hp():
    g = Gunner(270)
    assert g.hp == GUNNER_HP


def test_gunner_points():
    g = Gunner(270)
    assert g.points == GUNNER_POINTS


def test_gunner_spawns_off_top():
    g = Gunner(270)
    assert g.rect.bottom <= 0


def test_gunner_shoot_returns_three_bullets():
    g = Gunner(270)
    bullets = g.shoot(GUNNER_SHOOT_INTERVAL)
    assert len(bullets) == 3
    assert all(isinstance(b, EnemyBullet) for b in bullets)


def test_gunner_shoot_respects_cooldown():
    g = Gunner(270)
    g.shoot(GUNNER_SHOOT_INTERVAL)
    assert g.shoot(GUNNER_SHOOT_INTERVAL) == []


def test_gunner_shoot_spread_has_center_bullet():
    g = Gunner(270)
    bullets = g.shoot(GUNNER_SHOOT_INTERVAL)
    center_x = g.rect.centerx
    assert any(abs(b.rect.centerx - center_x) < 5 for b in bullets)


def test_gunner_moves_down():
    g = Gunner(270)
    initial_y = g.y
    g.update(1.0)
    assert g.y > initial_y


def test_gunner_take_damage():
    g = Gunner(270)
    g.take_damage(1)
    assert g.hp == GUNNER_HP - 1


def test_gunner_dies_when_hp_zero():
    g = Gunner(270)
    g.take_damage(GUNNER_HP)
    assert not g.alive()


# --- Striker ---

def test_striker_initial_hp():
    s = Striker(270)
    assert s.hp == STRIKER_HP


def test_striker_points():
    s = Striker(270)
    assert s.points == STRIKER_POINTS


def test_striker_spawns_off_top():
    s = Striker(270)
    assert s.rect.bottom <= 0


def test_striker_shoot_returns_two_bullets():
    s = Striker(270)
    bullets = s.shoot(STRIKER_SHOOT_INTERVAL)
    assert len(bullets) == 2
    assert all(isinstance(b, EnemyBullet) for b in bullets)


def test_striker_shoot_respects_cooldown():
    s = Striker(270)
    s.shoot(STRIKER_SHOOT_INTERVAL)
    assert s.shoot(STRIKER_SHOOT_INTERVAL) == []


def test_striker_diagonal_entry_from_left():
    s = Striker(100)
    initial_x = s.x
    s.update(0.1)
    assert s.x > initial_x


def test_striker_diagonal_entry_from_right():
    s = Striker(SCREEN_W - 100)
    initial_x = s.x
    s.update(0.1)
    assert s.x < initial_x


def test_striker_straight_down_past_entry_y():
    s = Striker(270)
    s.y = float(STRIKER_ENTRY_Y + 10)
    s.rect.y = int(s.y)
    initial_x = s.x
    s.update(0.1)
    assert abs(s.x - initial_x) < 0.01


def test_striker_moves_down():
    s = Striker(270)
    initial_y = s.y
    s.update(1.0)
    assert s.y > initial_y


# --- Interceptor ---

def test_interceptor_initial_hp():
    i = Interceptor(270)
    assert i.hp == INTERCEPTOR_HP


def test_interceptor_points():
    i = Interceptor(270)
    assert i.points == INTERCEPTOR_POINTS


def test_interceptor_spawns_off_top():
    i = Interceptor(270)
    assert i.rect.bottom <= 0


def test_interceptor_descends_to_y_target():
    i = Interceptor(270)
    for _ in range(200):
        i.update(0.05)
    assert abs(i.y - INTERCEPTOR_Y_TARGET) < 5


def test_interceptor_no_shoot_during_entry():
    i = Interceptor(270)
    assert i.shoot(INTERCEPTOR_SHOOT_INTERVAL) == []


def test_interceptor_shoot_after_entry():
    i = Interceptor(270)
    i._entry_done = True
    bullets = i.shoot(INTERCEPTOR_SHOOT_INTERVAL)
    assert len(bullets) == 1
    assert isinstance(bullets[0], EnemyBullet)


def test_interceptor_shoot_respects_cooldown():
    i = Interceptor(270)
    i._entry_done = True
    i.shoot(INTERCEPTOR_SHOOT_INTERVAL)
    assert i.shoot(INTERCEPTOR_SHOOT_INTERVAL) == []


def test_interceptor_patrols_horizontally():
    i = Interceptor(270)
    i._entry_done = True
    i.y = float(INTERCEPTOR_Y_TARGET)
    i.rect.y = int(i.y)
    initial_x = i.x
    i.update(0.5)
    assert i.x != initial_x


def test_interceptor_bounces_off_right_wall():
    i = Interceptor(270)
    i._entry_done = True
    i._dir_x = 1.0
    i.x = float(SCREEN_W - 5)
    i.rect.x = int(i.x)
    i.update(0.1)
    assert i._dir_x == -1.0


def test_interceptor_bounces_off_left_wall():
    i = Interceptor(270)
    i._entry_done = True
    i._dir_x = -1.0
    i.x = 0.0
    i.rect.x = 0
    i.update(0.1)
    assert i._dir_x == 1.0
