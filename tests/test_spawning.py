import pygame
from unittest.mock import patch
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.kamikaze import Kamikaze
from src.entities.boss import Boss
from src.systems.spawning import SpawnSystem
from src.settings import (
    WAVE_SPAWN_MIN, WAVE_TIME_THRESHOLD,
    WAVE_KILL_THRESHOLD, WAVE_FIGHTER_CAP,
    WAVE_KAMIKAZE_CAP,
    BOSS_WAVE_INTERVAL, BOSS_SPRITES, BOSS_SPRITES_FIXED_COUNT,
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


def test_make_enemy_returns_kamikaze():
    ss = SpawnSystem()
    with patch("src.systems.spawning.random.randint", side_effect=[270, 1]):
        enemy = ss._make_enemy()
    assert isinstance(enemy, Kamikaze)


def test_make_enemy_returns_scout_when_probs_low():
    ss = SpawnSystem()
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


def test_get_boss_spawn_returns_none_before_wave_trigger():
    ss = SpawnSystem()
    ss.wave = BOSS_WAVE_INTERVAL - 1
    assert ss.get_boss_spawn() is None


def test_get_boss_spawn_returns_boss_at_wave_trigger():
    ss = SpawnSystem()
    ss.wave = BOSS_WAVE_INTERVAL
    boss = ss.get_boss_spawn()
    assert isinstance(boss, Boss)


def test_get_boss_spawn_returns_none_while_boss_alive():
    ss = SpawnSystem()
    ss.wave = BOSS_WAVE_INTERVAL
    ss.get_boss_spawn()
    assert ss.get_boss_spawn() is None


def test_boss_alive_true_after_spawn():
    ss = SpawnSystem()
    ss.wave = BOSS_WAVE_INTERVAL
    ss.get_boss_spawn()
    assert ss.boss_alive is True


def test_notify_boss_killed_clears_boss_alive():
    ss = SpawnSystem()
    ss.wave = BOSS_WAVE_INTERVAL
    ss.get_boss_spawn()
    ss.notify_boss_killed()
    assert ss.boss_alive is False


def test_next_boss_spawns_after_next_wave_interval():
    ss = SpawnSystem()
    ss.wave = BOSS_WAVE_INTERVAL
    ss.get_boss_spawn()
    ss.notify_boss_killed()
    ss.wave = BOSS_WAVE_INTERVAL * 2 - 1
    assert ss.get_boss_spawn() is None
    ss.wave = BOSS_WAVE_INTERVAL * 2
    assert isinstance(ss.get_boss_spawn(), Boss)


def test_update_returns_empty_while_boss_alive():
    ss = SpawnSystem()
    ss.boss_alive = True
    ss._last_spawn = 0
    assert ss.update(99999) == []


def test_first_boss_does_not_use_random_choice():
    ss = SpawnSystem()
    ss.wave = BOSS_WAVE_INTERVAL
    with patch("src.systems.spawning.random.choice") as mock_choice:
        ss.get_boss_spawn()
    mock_choice.assert_not_called()


def test_fourth_boss_uses_random_choice():
    ss = SpawnSystem()
    for _ in range(BOSS_SPRITES_FIXED_COUNT):
        ss._boss_wave_at = ss.wave
        ss.get_boss_spawn()
        ss.notify_boss_killed()
    ss._boss_wave_at = ss.wave
    with patch("src.systems.spawning.random.choice", return_value=BOSS_SPRITES[0]) as mock_choice:
        ss.get_boss_spawn()
    mock_choice.assert_called_once_with(BOSS_SPRITES)
