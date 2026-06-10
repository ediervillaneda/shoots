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
    ss = SpawnSystem()
    now = ss._last_spawn + WAVE_SPAWN_MIN
    result = ss.update(now)
    assert len(result) == 1
    assert isinstance(result[0], (Scout, Fighter))


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
