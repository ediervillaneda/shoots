"""Tests for v1.9.0 — Modos de juego: Endless, Survival, Daily; nuevo enemigo Orbiter."""
import math
import random
import pytest
import pygame
from src.entities.orbiter import Orbiter
from src.entities.enemy_bullet import EnemyBullet
from src.scenes.mode_select import ModeSelectScene
from src.scenes.gameplay import GameplayScene
from src.settings import (
    ORBITER_RADIUS, ORBITER_HP, ORBITER_SHOOT_INTERVAL,
    SURVIVAL_TIME_MS, MODE_ENDLESS, MODE_SURVIVAL, MODE_DAILY,
)


@pytest.fixture(autouse=True)
def pg():
    # pygame is initialized at session scope by conftest.pygame_init
    yield


# ---- Orbiter ----

class TestOrbiter:
    def test_initial_position_on_orbit(self):
        o = Orbiter(270, 200, start_angle=0.0)
        expected_x = 270 + math.cos(0.0) * ORBITER_RADIUS - o.rect.width / 2
        assert abs(o.x - expected_x) < 1.0

    def test_position_changes_after_update(self):
        o = Orbiter(270, 200, start_angle=0.0)
        x_before = o.x
        o.update(0.1)
        assert o.x != x_before

    def test_hp_initial(self):
        o = Orbiter(270, 200)
        assert o.hp == ORBITER_HP

    def test_shoot_returns_empty_before_interval(self):
        o = Orbiter(270, 200)
        o.last_shot = 0
        result = o.shoot(ORBITER_SHOOT_INTERVAL - 1)
        assert result == []

    def test_shoot_returns_bullet_after_interval(self):
        o = Orbiter(270, 200)
        o.last_shot = 0
        result = o.shoot(ORBITER_SHOOT_INTERVAL)
        assert len(result) == 1
        assert isinstance(result[0], EnemyBullet)

    def test_take_damage_reduces_hp(self):
        o = Orbiter(270, 200)
        o.take_damage(3)
        assert o.hp == ORBITER_HP - 3

    def test_take_damage_kills_when_zero(self):
        o = Orbiter(270, 200)
        o.take_damage(ORBITER_HP)
        assert not o.alive()

    def test_different_start_angles_give_different_positions(self):
        o1 = Orbiter(270, 200, start_angle=0.0)
        o2 = Orbiter(270, 200, start_angle=math.pi)
        assert o1.x != o2.x


# ---- ModeSelectScene ----

class TestModeSelectScene:
    def test_instantiates(self):
        class FakeGame:
            def pop_scene(self): pass
        scene = ModeSelectScene(FakeGame())
        assert scene._selected == 0

    def test_key_down_increments_selected(self):
        class FakeGame:
            def pop_scene(self): pass
        scene = ModeSelectScene(FakeGame())
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
        scene.process_input([event])
        assert scene._selected == 1

    def test_key_up_wraps(self):
        class FakeGame:
            def pop_scene(self): pass
        scene = ModeSelectScene(FakeGame())
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode="")
        scene.process_input([event])
        assert scene._selected == 2  # wrap to last


# ---- GameplayScene modos ----

class TestGameplayModes:
    def test_endless_mode_default(self):
        g = GameplayScene(game=None, mode=MODE_ENDLESS)
        assert g._mode == MODE_ENDLESS

    def test_survival_mode_sets_timer(self):
        g = GameplayScene(game=None, mode=MODE_SURVIVAL)
        assert g._mode == MODE_SURVIVAL
        assert g._time_left_ms == SURVIVAL_TIME_MS

    def test_daily_mode_sets_mode(self):
        g = GameplayScene(game=None, mode=MODE_DAILY)
        assert g._mode == MODE_DAILY

    def test_survival_timer_decrements(self):
        g = GameplayScene(game=None, mode=MODE_SURVIVAL)
        initial = g._time_left_ms
        g.update(1.0)
        assert g._time_left_ms < initial

    def test_survival_game_over_when_timer_expires(self):
        g = GameplayScene(game=None, mode=MODE_SURVIVAL)
        g._time_left_ms = 10.0   # casi nada
        g.update(0.1)            # 100ms — suficiente para llegar a 0
        assert g.state == "game_over"
