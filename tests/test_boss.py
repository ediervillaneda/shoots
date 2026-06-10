import pytest
import pygame
from src.entities.boss import Boss
from src.entities.enemy_bullet import EnemyBullet
from src.settings import (
    SCREEN_W, BOSS_HP, BOSS_W, BOSS_Y_TARGET,
    BOSS_SHOOT_INTERVAL_P1, BOSS_SHOOT_INTERVAL_P2,
    BOSS_SPRITES,
)

SPRITE = BOSS_SPRITES[0]


def test_boss_spawns_at_top_center():
    boss = Boss(SPRITE)
    assert boss.rect.centerx == SCREEN_W // 2
    assert boss.rect.bottom == 0


def test_boss_descends_during_entry():
    boss = Boss(SPRITE)
    initial_y = boss.y
    boss.update(0.5)
    assert boss.y > initial_y


def test_boss_entry_completes_at_y_target():
    boss = Boss(SPRITE)
    boss.y = BOSS_Y_TARGET
    boss.update(0.0)
    assert boss._entry_done is True


def test_boss_ping_pong_moves_right_initially():
    boss = Boss(SPRITE)
    boss._entry_done = True
    initial_x = boss.x
    boss.update(0.1)
    assert boss.x > initial_x


def test_boss_bounces_at_right_edge():
    boss = Boss(SPRITE)
    boss._entry_done = True
    boss.dir = 1
    boss.x = float(SCREEN_W - BOSS_W + 1)
    boss.rect.x = SCREEN_W - BOSS_W + 1
    boss.update(0.0)
    assert boss.dir == -1


def test_boss_bounces_at_left_edge():
    boss = Boss(SPRITE)
    boss._entry_done = True
    boss.dir = -1
    boss.x = -1.0
    boss.rect.x = -1
    boss.update(0.0)
    assert boss.dir == 1


def test_boss_starts_phase_1():
    boss = Boss(SPRITE)
    assert boss.phase == 1


def test_boss_transitions_to_phase_2_at_half_hp():
    boss = Boss(SPRITE)
    boss.hp = BOSS_HP // 2
    boss.update(0.0)
    assert boss.phase == 2


def test_boss_shoot_phase1_returns_one_bullet():
    boss = Boss(SPRITE)
    bullets = boss.shoot(BOSS_SHOOT_INTERVAL_P1)
    assert len(bullets) == 1
    assert isinstance(bullets[0], EnemyBullet)


def test_boss_shoot_phase2_returns_three_bullets():
    boss = Boss(SPRITE)
    boss.phase = 2
    boss.last_shot = -BOSS_SHOOT_INTERVAL_P2
    bullets = boss.shoot(0)
    assert len(bullets) == 3
    assert all(isinstance(b, EnemyBullet) for b in bullets)


def test_boss_shoot_respects_cooldown():
    boss = Boss(SPRITE)
    boss.shoot(BOSS_SHOOT_INTERVAL_P1)
    assert boss.shoot(BOSS_SHOOT_INTERVAL_P1) == []


def test_boss_stays_alive_inside_screen():
    boss = Boss(SPRITE)
    boss._entry_done = True
    group = pygame.sprite.Group(boss)
    boss.update(0.016)
    assert boss.alive()
