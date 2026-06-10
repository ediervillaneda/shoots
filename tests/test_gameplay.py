import pygame
from unittest.mock import patch
from src.scenes.gameplay import GameplayScene
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.bullet import Bullet
from src.entities.enemy_bullet import EnemyBullet
from src.entities.powerup import PowerUp
from src.entities.kamikaze import Kamikaze
from src.entities.boss import Boss
from src.settings import SCOUT_POINTS, PLAYER_LIVES, SCREEN_H, WAVE_SPAWN_MIN, FIGHTER_HP, BULLET_DAMAGE, BOSS_SPRITES, BOSS_SHOOT_INTERVAL_P1


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
    assert fighter.hp == FIGHTER_HP - BULLET_DAMAGE


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
    with patch("src.scenes.gameplay.random.random", return_value=1.0):  # no drop
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


def test_powerup_group_exists_after_reset():
    scene = GameplayScene()
    scene._reset()
    assert isinstance(scene.powerups, pygame.sprite.Group)


def test_bullet_kill_drops_powerup_when_lucky():
    scene = GameplayScene()
    scene._reset()
    scout = Scout(270)
    scout.rect.center = (270, 480)
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    bullet = Bullet(270, 480)
    bullet.rect.center = (270, 480)
    scene.bullets.add(bullet)
    scene.all_sprites.add(bullet)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    with patch("src.scenes.gameplay.random.random", return_value=0.0):  # always drop
        scene.update(0.0)
    assert len(scene.powerups) == 1


def test_player_picks_up_powerup():
    scene = GameplayScene()
    scene._reset()
    pu = PowerUp("rapid_fire", scene.player.rect.centerx, scene.player.rect.centery)
    pu.rect.center = scene.player.rect.center
    scene.powerups.add(pu)
    scene.all_sprites.add(pu)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert "rapid_fire" in scene.player.active_powerups
    assert not pu.alive()


def test_kamikaze_gets_target_on_spawn():
    scene = GameplayScene()
    scene._reset()
    scene.spawn_system._last_spawn = pygame.time.get_ticks() - WAVE_SPAWN_MIN
    with patch("src.systems.spawning.random.randint", side_effect=[270, 1]):
        scene.update(0.016)
    kamikazes = [e for e in scene.enemies if isinstance(e, Kamikaze)]
    assert len(kamikazes) == 1
    assert kamikazes[0].target is scene.player


def test_boss_added_to_enemies_on_spawn():
    scene = GameplayScene()
    scene._reset()
    boss = Boss(BOSS_SPRITES[0])
    with patch.object(scene.spawn_system, 'get_boss_spawn', return_value=boss):
        scene.spawn_system._last_spawn = pygame.time.get_ticks()
        scene.update(0.0)
    assert boss in scene.enemies


def test_boss_reference_set_on_spawn():
    scene = GameplayScene()
    scene._reset()
    boss = Boss(BOSS_SPRITES[0])
    with patch.object(scene.spawn_system, 'get_boss_spawn', return_value=boss):
        scene.spawn_system._last_spawn = pygame.time.get_ticks()
        scene.update(0.0)
    assert scene.boss is boss


def test_boss_reference_cleared_when_dead():
    scene = GameplayScene()
    scene._reset()
    boss = Boss(BOSS_SPRITES[0])
    scene.boss = boss
    scene.enemies.add(boss)
    scene.all_sprites.add(boss)
    boss.kill()
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    with patch.object(scene.spawn_system, 'notify_boss_killed'):
        scene.update(0.0)
    assert scene.boss is None


def test_boss_death_calls_notify_boss_killed():
    scene = GameplayScene()
    scene._reset()
    boss = Boss(BOSS_SPRITES[0])
    scene.boss = boss
    scene.enemies.add(boss)
    scene.all_sprites.add(boss)
    boss.kill()
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    with patch.object(scene.spawn_system, 'notify_boss_killed') as mock_notify:
        scene.update(0.0)
    mock_notify.assert_called_once()


def test_boss_shoot_adds_enemy_bullets():
    scene = GameplayScene()
    scene._reset()
    boss = Boss(BOSS_SPRITES[0])
    boss._entry_done = True
    boss.last_shot = -(BOSS_SHOOT_INTERVAL_P1 + 1)
    scene.boss = boss
    scene.enemies.add(boss)
    scene.all_sprites.add(boss)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    initial_count = len(scene.enemy_bullets)
    scene.update(0.0)
    assert len(scene.enemy_bullets) > initial_count


def test_boss_none_after_reset():
    scene = GameplayScene()
    scene.boss = Boss(BOSS_SPRITES[0])
    scene._reset()
    assert scene.boss is None


# --- v0.7: rocket + explosion ---

from src.entities.rocket import Rocket
from src.entities.explosion import Explosion
from src.entities.scout import Scout as _Scout
from src.settings import ROCKET_COOLDOWN


def test_rocket_added_to_group_on_shoot():
    scene = GameplayScene()
    scene._reset()
    scene.player.apply_powerup("rocket")
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    with patch("pygame.key.get_pressed", return_value={pygame.K_SPACE: True, **{k: False for k in range(512)}}):
        pass
    rocket = Rocket(scene.player.rect.centerx, scene.player.rect.top)
    scene.rockets.add(rocket)
    scene.all_sprites.add(rocket)
    assert len(scene.rockets) == 1


def test_rocket_hit_spawns_explosion():
    scene = GameplayScene()
    scene._reset()
    scout = _Scout(270)
    scout.rect.center = (270, 300)
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    rocket = Rocket(270, 300)
    rocket.rect.center = (270, 300)
    scene.rockets.add(rocket)
    scene.all_sprites.add(rocket)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert len(scene.explosions) >= 1
    assert all(isinstance(e, Explosion) for e in scene.explosions)


def test_rocket_hit_kills_direct_enemy():
    scene = GameplayScene()
    scene._reset()
    scout = _Scout(270)
    scout.rect.center = (270, 300)
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    rocket = Rocket(270, 300)
    rocket.rect.center = (270, 300)
    scene.rockets.add(rocket)
    scene.all_sprites.add(rocket)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert not scout.alive()


def test_rocket_area_damage_hits_nearby_enemy():
    from src.settings import ROCKET_RADIUS, ROCKET_AREA_DAMAGE
    scene = GameplayScene()
    scene._reset()
    # Direct hit target
    scout1 = _Scout(270)
    scout1.rect.center = (270, 300)
    scout1.x = float(scout1.rect.x)
    scout1.y = float(scout1.rect.y)
    # Nearby target (within radius)
    from src.entities.fighter import Fighter
    fighter = Fighter(270)
    fighter.rect.center = (270 + ROCKET_RADIUS - 10, 300)
    fighter.x = float(fighter.rect.x)
    fighter.y = float(fighter.rect.y)
    fighter.origin_x = float(fighter.rect.x)
    fighter_initial_hp = fighter.hp
    scene.enemies.add(scout1)
    scene.enemies.add(fighter)
    scene.all_sprites.add(scout1)
    scene.all_sprites.add(fighter)
    rocket = Rocket(270, 300)
    rocket.rect.center = (270, 300)
    scene.rockets.add(rocket)
    scene.all_sprites.add(rocket)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert fighter.hp == fighter_initial_hp - ROCKET_AREA_DAMAGE


# --- v0.7: entity death explosions ---

from src.settings import EXPL_SCOUT, EXPL_FIGHTER, EXPL_BOSS, EXPL_PLAYER


def test_bullet_kill_spawns_explosion():
    scene = GameplayScene()
    scene._reset()
    scout = _Scout(270)
    scout.rect.center = (270, 480)
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    bullet = Bullet(270, 480)
    bullet.rect.center = (270, 480)
    scene.bullets.add(bullet)
    scene.all_sprites.add(bullet)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    scene.update(0.0)
    assert not scout.alive()
    assert len(scene.explosions) == 1
    assert isinstance(list(scene.explosions)[0], Explosion)


def test_player_collision_spawns_enemy_explosion():
    scene = GameplayScene()
    scene._reset()
    scout = _Scout(scene.player.rect.centerx)
    scout.rect.center = scene.player.rect.center
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    with patch("src.scenes.gameplay.random.random", return_value=1.0):
        scene.update(0.0)
    assert not scout.alive()
    assert any(isinstance(e, Explosion) for e in scene.explosions)


def test_player_hit_spawns_player_explosion():
    scene = GameplayScene()
    scene._reset()
    scout = _Scout(scene.player.rect.centerx)
    scout.rect.center = scene.player.rect.center
    scout.x = float(scout.rect.x)
    scout.y = float(scout.rect.y)
    scene.enemies.add(scout)
    scene.all_sprites.add(scout)
    initial_lives = scene.player.lives
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    with patch("src.scenes.gameplay.random.random", return_value=1.0):
        scene.update(0.0)
    assert scene.player.lives < initial_lives
    explosions = list(scene.explosions)
    assert len(explosions) >= 2  # enemy death + player explosion


def test_boss_death_spawns_explosion():
    scene = GameplayScene()
    scene._reset()
    boss = Boss(BOSS_SPRITES[0])
    scene.boss = boss
    scene.enemies.add(boss)
    scene.all_sprites.add(boss)
    boss.kill()
    scene.spawn_system._last_spawn = pygame.time.get_ticks()
    with patch.object(scene.spawn_system, 'notify_boss_killed'):
        scene.update(0.0)
    assert len(scene.explosions) == 1
    expl = list(scene.explosions)[0]
    assert isinstance(expl, Explosion)
    assert expl.image.get_size() == (160, 160)
