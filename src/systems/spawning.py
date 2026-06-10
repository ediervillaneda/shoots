import random
import pygame
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.kamikaze import Kamikaze
from src.entities.boss import Boss
from src.settings import (
    SCREEN_W, SCOUT_W, FIGHTER_W,
    WAVE_TIME_THRESHOLD, WAVE_KILL_THRESHOLD,
    WAVE_SPAWN_MIN, WAVE_SPAWN_MIN_CAP,
    WAVE_FIGHTER_BASE, WAVE_FIGHTER_INC, WAVE_FIGHTER_CAP,
    WAVE_KAMIKAZE_BASE, WAVE_KAMIKAZE_INC, WAVE_KAMIKAZE_CAP,
    WAVE_SPEED_FACTOR,
    BOSS_TRIGGER_MS, BOSS_SPRITES, BOSS_SPRITES_FIXED_COUNT,
)


class SpawnSystem:
    def __init__(self):
        self.wave = 0
        self.kills = 0
        self._last_spawn = pygame.time.get_ticks()
        self._wave_start = pygame.time.get_ticks()
        self._boss_spawn_at: int = BOSS_TRIGGER_MS
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

    def get_boss_spawn(self, now: int):
        if self.boss_alive or now < self._boss_spawn_at:
            return None
        sprite = self._next_boss_sprite()
        self._boss_index += 1
        self.boss_alive = True
        return Boss(sprite)

    def notify_boss_killed(self, now: int) -> None:
        self.boss_alive = False
        self._boss_spawn_at = now + BOSS_TRIGGER_MS

    def _next_boss_sprite(self) -> str:
        if self._boss_index < BOSS_SPRITES_FIXED_COUNT:
            return BOSS_SPRITES[self._boss_index]
        return random.choice(BOSS_SPRITES)

    def _spawn_interval(self):
        return max(WAVE_SPAWN_MIN_CAP, WAVE_SPAWN_MIN - self.wave * 150)

    def _kamikaze_prob(self):
        return min(WAVE_KAMIKAZE_CAP, WAVE_KAMIKAZE_BASE + self.wave * WAVE_KAMIKAZE_INC)

    def _fighter_prob(self):
        return min(WAVE_FIGHTER_CAP, WAVE_FIGHTER_BASE + self.wave * WAVE_FIGHTER_INC)

    def _make_enemy(self):
        margin = max(SCOUT_W, FIGHTER_W) // 2
        x = random.randint(margin, SCREEN_W - margin)
        speed_bonus = self.wave * WAVE_SPEED_FACTOR
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
