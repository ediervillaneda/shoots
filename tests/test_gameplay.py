import pygame
from src.scenes.gameplay import GameplayScene
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.bullet import Bullet


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
    scout = Scout(240)
    scout.rect.center = (240, 320)
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
    fighter = Fighter(240)
    fighter.rect.center = (240, 320)
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
    assert fighter.hp == 2
