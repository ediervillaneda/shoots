import random
import pygame
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.settings import (
    SCREEN_W, SCOUT_W, FIGHTER_W,
    WAVE_TIME_THRESHOLD, WAVE_KILL_THRESHOLD,
    WAVE_SPAWN_MIN, WAVE_SPAWN_MIN_CAP,
    WAVE_FIGHTER_BASE, WAVE_FIGHTER_INC, WAVE_FIGHTER_CAP,
    WAVE_SPEED_FACTOR,
)


class SpawnSystem:
    def __init__(self):
        self.wave = 0
        self.kills = 0
        # pygame must be initialized before constructing SpawnSystem
        self._last_spawn = pygame.time.get_ticks()
        self._wave_start = pygame.time.get_ticks()

    def register_kill(self):
        self.kills += 1
        # wave advances every WAVE_KILL_THRESHOLD cumulative kills (intentional unbounded scaling)
        if self.wave >= 3 and self.kills % WAVE_KILL_THRESHOLD == 0:
            self.wave += 1

    def update(self, now):
        """Returns list with one new Enemy if spawn interval elapsed, else [].
        One spawn and at most one wave advance per call — by design."""
        if self.wave < 3:
            if now - self._wave_start >= WAVE_TIME_THRESHOLD:
                self.wave += 1
                self._wave_start = now

        if now - self._last_spawn >= self._spawn_interval():
            self._last_spawn = now
            return [self._make_enemy()]
        return []

    def _spawn_interval(self):
        return max(WAVE_SPAWN_MIN_CAP, WAVE_SPAWN_MIN - self.wave * 150)

    def _fighter_prob(self):
        return min(WAVE_FIGHTER_CAP, WAVE_FIGHTER_BASE + self.wave * WAVE_FIGHTER_INC)

    def _make_enemy(self):
        margin = max(SCOUT_W, FIGHTER_W) // 2
        x = random.randint(margin, SCREEN_W - margin)
        speed_bonus = self.wave * WAVE_SPEED_FACTOR
        if random.randint(1, 100) <= self._fighter_prob():
            f = Fighter(x)
            f.speed_bonus = speed_bonus
            return f
        s = Scout(x)
        s.speed_bonus = speed_bonus
        return s
