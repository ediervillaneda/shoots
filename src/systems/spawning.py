import random
import pygame
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.kamikaze import Kamikaze
from src.entities.gunner import Gunner
from src.entities.striker import Striker
from src.entities.interceptor import Interceptor
from src.entities.boss import Boss
from src.settings import (
    SCREEN_W, SCOUT_W, FIGHTER_W,
    WAVE_TIME_THRESHOLD, WAVE_KILL_THRESHOLD,
    WAVE_SPAWN_MIN, WAVE_SPAWN_MIN_CAP, WAVE_SPAWN_DEC,
    WAVE_FIGHTER_BASE, WAVE_FIGHTER_INC, WAVE_FIGHTER_CAP,
    WAVE_KAMIKAZE_BASE, WAVE_KAMIKAZE_INC, WAVE_KAMIKAZE_CAP,
    WAVE_GUNNER_MIN_WAVE, WAVE_GUNNER_BASE, WAVE_GUNNER_INC, WAVE_GUNNER_CAP,
    WAVE_STRIKER_MIN_WAVE, WAVE_STRIKER_BASE, WAVE_STRIKER_INC, WAVE_STRIKER_CAP,
    WAVE_INTERCEPTOR_MIN_WAVE, WAVE_INTERCEPTOR_BASE, WAVE_INTERCEPTOR_INC, WAVE_INTERCEPTOR_CAP,
    WAVE_SPEED_FACTOR,
    BOSS_WAVE_INTERVAL, BOSS_SPRITES, BOSS_SPRITES_FIXED_COUNT,
)


class SpawnSystem:
    def __init__(self):
        self.wave = 0
        self.kills = 0
        self._last_spawn = pygame.time.get_ticks()
        self._wave_start = pygame.time.get_ticks()
        self._boss_wave_at: int = BOSS_WAVE_INTERVAL
        self._boss_index: int = 0
        self.boss_alive: bool = False

    def register_kill(self):
        self.kills += 1
        if self.wave >= 3 and self.kills % WAVE_KILL_THRESHOLD == 0:
            self.wave += 1

    def update(self, now: int) -> list:
        if self.boss_alive:
            return []
        if self.wave < 3:
            if now - self._wave_start >= WAVE_TIME_THRESHOLD:
                self.wave += 1
                self._wave_start = now
        if now - self._last_spawn >= self._spawn_interval():
            self._last_spawn = now
            return [self._make_enemy()]
        return []

    def get_boss_spawn(self):
        if self.boss_alive or self.wave < self._boss_wave_at:
            return None
        sprite = self._next_boss_sprite()
        self._boss_index += 1
        self.boss_alive = True
        return Boss(sprite)

    def notify_boss_killed(self) -> None:
        self.boss_alive = False
        self._boss_wave_at = self.wave + BOSS_WAVE_INTERVAL

    def _next_boss_sprite(self) -> str:
        if self._boss_index < BOSS_SPRITES_FIXED_COUNT:
            return BOSS_SPRITES[self._boss_index]
        return random.choice(BOSS_SPRITES)

    def _spawn_interval(self):
        return max(WAVE_SPAWN_MIN_CAP, WAVE_SPAWN_MIN - self.wave * WAVE_SPAWN_DEC)

    def _kamikaze_prob(self):
        return min(WAVE_KAMIKAZE_CAP, WAVE_KAMIKAZE_BASE + self.wave * WAVE_KAMIKAZE_INC)

    def _fighter_prob(self):
        return min(WAVE_FIGHTER_CAP, WAVE_FIGHTER_BASE + self.wave * WAVE_FIGHTER_INC)

    def _gunner_prob(self):
        return min(WAVE_GUNNER_CAP, WAVE_GUNNER_BASE + (self.wave - WAVE_GUNNER_MIN_WAVE) * WAVE_GUNNER_INC)

    def _striker_prob(self):
        return min(WAVE_STRIKER_CAP, WAVE_STRIKER_BASE + (self.wave - WAVE_STRIKER_MIN_WAVE) * WAVE_STRIKER_INC)

    def _interceptor_prob(self):
        return min(WAVE_INTERCEPTOR_CAP, WAVE_INTERCEPTOR_BASE + (self.wave - WAVE_INTERCEPTOR_MIN_WAVE) * WAVE_INTERCEPTOR_INC)

    def _make_enemy(self):
        margin = max(SCOUT_W, FIGHTER_W) // 2
        x = random.randint(margin, SCREEN_W - margin)
        speed_bonus = self.wave * WAVE_SPEED_FACTOR
        if self.wave >= WAVE_INTERCEPTOR_MIN_WAVE and random.randint(1, 100) <= self._interceptor_prob():
            e = Interceptor(x)
            e.speed_bonus = speed_bonus
            return e
        if self.wave >= WAVE_STRIKER_MIN_WAVE and random.randint(1, 100) <= self._striker_prob():
            e = Striker(x)
            e.speed_bonus = speed_bonus
            return e
        if self.wave >= WAVE_GUNNER_MIN_WAVE and random.randint(1, 100) <= self._gunner_prob():
            e = Gunner(x)
            e.speed_bonus = speed_bonus
            return e
        if random.randint(1, 100) <= self._kamikaze_prob():
            k = Kamikaze(x)
            k.speed_bonus = speed_bonus
            return k
        if random.randint(1, 100) <= self._fighter_prob():
            f = Fighter(x)
            f.speed_bonus = speed_bonus
            return f
        s = Scout(x)
        s.speed_bonus = speed_bonus
        return s
