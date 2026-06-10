import pygame
from src.entities.enemy import Enemy
from src.settings import SCREEN_H


def make_enemy():
    return Enemy(x=240, w=40, h=40, color=(255, 0, 0), hp=2, points=100)


def test_enemy_initial_hp():
    e = make_enemy()
    assert e.hp == 2


def test_take_damage_reduces_hp():
    e = make_enemy()
    e.take_damage(1)
    assert e.hp == 1


def test_take_damage_kills_at_zero():
    e = make_enemy()
    group = pygame.sprite.Group(e)
    e.take_damage(2)
    assert not e.alive()


def test_take_damage_kills_on_overkill():
    e = make_enemy()
    group = pygame.sprite.Group(e)
    e.take_damage(10)
    assert not e.alive()


def test_enemy_killed_when_below_screen():
    e = make_enemy()
    group = pygame.sprite.Group(e)
    e.rect.top = SCREEN_H + 1
    e.update(0.016)
    assert not e.alive()


def test_enemy_alive_when_on_screen():
    e = make_enemy()
    group = pygame.sprite.Group(e)
    e.rect.top = SCREEN_H // 2
    e.update(0.016)
    assert e.alive()


def test_enemy_spawns_above_screen():
    e = make_enemy()
    assert e.rect.bottom == 0


def test_enemy_centerx_matches_spawn_x():
    e = make_enemy()
    assert e.rect.centerx == 240
