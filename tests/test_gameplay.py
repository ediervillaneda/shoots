import pygame
from src.scenes.gameplay import GameplayScene
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.bullet import Bullet
from src.settings import SCOUT_POINTS, PLAYER_LIVES, SCREEN_H


# --- tests existentes (actualizados para state="playing") ---

def test_spawn_enemy_adds_to_enemies_group():
    scene = GameplayScene()
    scene.spawn_enemy()
    assert len(scene.enemies) == 1


def test_spawn_enemy_adds_to_all_sprites():
    scene = GameplayScene()
    initial = len(scene.all_sprites)
    scene.spawn_enemy()
    assert len(scene.all_sprites) == initial + 1


def test_spawn_produces_scout_or_fighter():
    scene = GameplayScene()
    scene.spawn_enemy()
    enemy = list(scene.enemies)[0]
    assert isinstance(enemy, (Scout, Fighter))


def test_bullet_kills_scout_on_collision():
    scene = GameplayScene()
    scene._reset()                          # state="playing"
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

    scene.last_spawn = pygame.time.get_ticks()
    scene.update(0.0)

    assert not bullet.alive()
    assert not scout.alive()


def test_bullet_damages_fighter_without_killing():
    scene = GameplayScene()
    scene._reset()                          # state="playing"
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

    scene.last_spawn = pygame.time.get_ticks()
    scene.update(0.0)

    assert not bullet.alive()
    assert fighter.alive()
    assert fighter.hp == 1


# --- tests nuevos v0.3 ---

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


def test_update_noop_when_not_playing():
    scene = GameplayScene()              # state="start"
    scout = Scout(270)
    scout.rect.top = SCREEN_H + 10      # fuera de pantalla: moriría si update corriera
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    scene.update(0.016)
    assert scout.alive()                # update() no corrió


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

    scene.last_spawn = pygame.time.get_ticks()
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

    scene.last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.score == 0
    assert fighter.alive()


def test_player_enemy_collision_scores():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(scene.player.rect.centerx)
    scout.rect.center = scene.player.rect.center
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)

    scene.last_spawn = pygame.time.get_ticks()
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

    scene.last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.player.lives == PLAYER_LIVES - 1


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

    scene.last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert scene.state == "game_over"
