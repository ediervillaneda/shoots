import pygame
from src.scenes.gameplay import GameplayScene
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.bullet import Bullet
from src.entities.enemy_bullet import EnemyBullet
from src.settings import SCOUT_POINTS, PLAYER_LIVES, SCREEN_H, WAVE_SPAWN_MIN


# --- tests de estado y reset ---

def test_initial_state_is_start():
    scene = GameplayScene()
    assert scene.state == "start"


def test_reset_sets_state_playing():
    scene = GameplayScene()
    scene._reset()
    assert scene.state == "playing"


def test_reset_zeroes_score():
    scene = GameplayScene()
    scene.score = 500
    scene._reset()
    assert scene.score == 0


def test_reset_restores_player():
    scene = GameplayScene()
    scene._reset()
    assert scene.player.lives == PLAYER_LIVES


def test_enemy_bullet_group_exists_after_reset():
    scene = GameplayScene()
    scene._reset()
    assert isinstance(scene.enemy_bullets, pygame.sprite.Group)


def test_spawn_system_created_on_reset():
    scene = GameplayScene()
    scene._reset()
    from src.systems.spawning import SpawnSystem
    assert isinstance(scene.spawn_system, SpawnSystem)


# --- test noop cuando no está playing ---

def test_update_noop_when_not_playing():
    scene = GameplayScene()              # state="start"
    scout = Scout(270)
    scout.rect.top = SCREEN_H + 10
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    scene.update(0.016)
    assert scout.alive()


# --- tests de balas del player ---

def test_bullet_kills_scout_on_collision():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(270)
    scout.rect.center = (270, 480)
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    bullet = Bullet(scout.rect.centerx, scout.rect.centery)
    bullet.rect.center = scout.rect.center
    scene.bullets.add(bullet)
    scene.all_sprites.add(bullet)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)

    assert not bullet.alive()
    assert not scout.alive()


def test_bullet_damages_fighter_without_killing():
    scene = GameplayScene()
    scene._reset()
    fighter = Fighter(270)
    fighter.rect.center = (270, 480)
    fighter.x = float(fighter.rect.x)
    fighter.y = float(fighter.rect.y)
    scene.enemies.add(fighter)
    scene.all_sprites.add(fighter)

    bullet = Bullet(fighter.rect.centerx, fighter.rect.centery)
    bullet.rect.center = fighter.rect.center
    scene.bullets.add(bullet)
    scene.all_sprites.add(bullet)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)

    assert not bullet.alive()
    assert fighter.alive()
    assert fighter.hp == 1


def test_bullet_scores_on_kill():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(270)
    scout.rect.center = (270, 480)
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    bullet = Bullet(scout.rect.centerx, scout.rect.centery)
    bullet.rect.center = scout.rect.center
    scene.bullets.add(bullet)
    scene.all_sprites.add(bullet)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.score == SCOUT_POINTS


def test_bullet_no_score_if_enemy_survives():
    scene = GameplayScene()
    scene._reset()
    fighter = Fighter(270)
    fighter.rect.center = (270, 480)
    fighter.x = float(fighter.rect.x)
    fighter.y = float(fighter.rect.y)
    scene.enemies.add(fighter)
    scene.all_sprites.add(fighter)

    bullet = Bullet(fighter.rect.centerx, fighter.rect.centery)
    bullet.rect.center = fighter.rect.center
    scene.bullets.add(bullet)
    scene.all_sprites.add(bullet)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.score == 0
    assert fighter.alive()


def test_bullet_kill_registers_with_spawn_system():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(270)
    scout.rect.center = (270, 480)
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    bullet = Bullet(scout.rect.centerx, scout.rect.centery)
    bullet.rect.center = scout.rect.center
    scene.bullets.add(bullet)
    scene.all_sprites.add(bullet)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.spawn_system.kills == 1


# --- tests colisión player ↔ enemies ---

def test_player_enemy_collision_scores():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(scene.player.rect.centerx)
    scout.rect.center = scene.player.rect.center
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.score == SCOUT_POINTS


def test_player_enemy_collision_damages_player():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(scene.player.rect.centerx)
    scout.rect.center = scene.player.rect.center
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.player.lives == PLAYER_LIVES - 1


def test_collision_kill_registers_with_spawn_system():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(scene.player.rect.centerx)
    scout.rect.center = scene.player.rect.center
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.spawn_system.kills == 1


def test_game_over_when_lives_reach_zero():
    scene = GameplayScene()
    scene._reset()
    scene.player.lives = 1
    scout = Scout(scene.player.rect.centerx)
    scout.rect.center = scene.player.rect.center
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.state == "game_over"


# --- tests balas enemigas ---

def test_enemy_bullet_damages_player():
    scene = GameplayScene()
    scene._reset()
    eb = EnemyBullet(scene.player.rect.centerx, scene.player.rect.centery)
    eb.rect.center = scene.player.rect.center
    scene.enemy_bullets.add(eb)
    scene.all_sprites.add(eb)
    initial_lives = scene.player.lives
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.player.lives == initial_lives - 1


def test_enemy_bullet_disappears_on_hit():
    scene = GameplayScene()
    scene._reset()
    eb = EnemyBullet(scene.player.rect.centerx, scene.player.rect.centery)
    eb.rect.center = scene.player.rect.center
    scene.enemy_bullets.add(eb)
    scene.all_sprites.add(eb)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert not eb.alive()


def test_spawn_system_adds_enemy_to_groups():
    scene = GameplayScene()
    scene._reset()
    scene.spawn_system._last_spawn = pygame.time.get_ticks() - WAVE_SPAWN_MIN
    initial_enemies = len(scene.enemies)
    scene.update(0.016)
    assert len(scene.enemies) > initial_enemies
