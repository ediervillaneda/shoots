import pygame
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.systems.spawning import SpawnSystem
from src.settings import (
    WAVE_SPAWN_MIN, WAVE_TIME_THRESHOLD,
    WAVE_KILL_THRESHOLD, WAVE_FIGHTER_CAP,
)


def test_spawn_system_starts_wave_zero():
    ss = SpawnSystem()
    assert ss.wave == 0


def test_spawn_system_starts_kills_zero():
    ss = SpawnSystem()
    assert ss.kills == 0


def test_spawn_returns_empty_before_interval():
    ss = SpawnSystem()
    result = ss.update(ss._last_spawn)
    assert result == []


def test_spawn_returns_enemy_on_interval():
    from src.entities.kamikaze import Kamikaze
    ss = SpawnSystem()
    ss._last_spawn = pygame.time.get_ticks() - WAVE_SPAWN_MIN
    result = ss.update(pygame.time.get_ticks())
    assert len(result) == 1
    assert isinstance(result[0], (Scout, Fighter, Kamikaze))


def test_wave_advances_by_time():
    ss = SpawnSystem()
    now = ss._wave_start + WAVE_TIME_THRESHOLD
    ss.update(now)
    assert ss.wave == 1


def test_wave_does_not_advance_before_threshold():
    ss = SpawnSystem()
    now = ss._wave_start + WAVE_TIME_THRESHOLD - 1
    ss.update(now)
    assert ss.wave == 0


def test_wave_advances_by_kills():
    ss = SpawnSystem()
    ss.wave = 3
    for _ in range(WAVE_KILL_THRESHOLD):
        ss.register_kill()
    assert ss.wave == 4


def test_kills_dont_advance_wave_below_3():
    ss = SpawnSystem()
    for _ in range(WAVE_KILL_THRESHOLD):
        ss.register_kill()
    assert ss.wave == 0


def test_spawn_interval_decreases_with_wave():
    ss = SpawnSystem()
    interval_wave0 = ss._spawn_interval()
    ss.wave = 3
    assert ss._spawn_interval() < interval_wave0


def test_fighter_prob_capped():
    ss = SpawnSystem()
    ss.wave = 100
    assert ss._fighter_prob() == WAVE_FIGHTER_CAP


from unittest.mock import patch
from src.entities.kamikaze import Kamikaze
from src.settings import WAVE_KAMIKAZE_BASE, WAVE_KAMIKAZE_INC, WAVE_KAMIKAZE_CAP


def test_make_enemy_returns_kamikaze():
    ss = SpawnSystem()
    # side_effect order: [x_position, kamikaze_prob_check]
    with patch("src.systems.spawning.random.randint", side_effect=[270, 1]):
        enemy = ss._make_enemy()
    assert isinstance(enemy, Kamikaze)


def test_make_enemy_returns_scout_when_probs_low():
    ss = SpawnSystem()
    # x=270, kamikaze_check=100 (fail, 100>10), fighter_check=100 (fail, 100>30) → Scout
    with patch("src.systems.spawning.random.randint", side_effect=[270, 100, 100]):
        enemy = ss._make_enemy()
    assert isinstance(enemy, Scout)


def test_kamikaze_prob_increases_with_wave():
    ss = SpawnSystem()
    prob_wave0 = ss._kamikaze_prob()
    ss.wave = 3
    assert ss._kamikaze_prob() > prob_wave0


def test_kamikaze_prob_capped():
    ss = SpawnSystem()
    ss.wave = 1000
    assert ss._kamikaze_prob() == WAVE_KAMIKAZE_CAP
