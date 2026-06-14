import pygame
from src.entities.enemy import Enemy
from src.settings import ENEMY_FLASH_MS


def test_flash_ms_zero_on_init():
    e = Enemy(x=270, w=40, h=40, color=(255, 0, 0), hp=3, points=100)
    assert e._flash_ms == 0.0


def test_take_damage_activates_flash_when_survives():
    e = Enemy(x=270, w=40, h=40, color=(255, 0, 0), hp=3, points=100)
    e.take_damage(1)
    assert e._flash_ms == ENEMY_FLASH_MS
    assert e.hp > 0  # sobrevivió


def test_take_damage_no_flash_when_dies():
    e = Enemy(x=270, w=40, h=40, color=(255, 0, 0), hp=1, points=100)
    e.take_damage(1)
    assert not e.alive()


def test_flash_decrements_on_update():
    e = Enemy(x=270, w=40, h=40, color=(255, 0, 0), hp=3, points=100)
    e.take_damage(1)
    initial = e._flash_ms
    e.update(0.05)  # 50 ms
    assert e._flash_ms < initial
