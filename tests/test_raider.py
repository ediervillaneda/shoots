import pygame
from src.entities.raider import Raider
from src.settings import SCREEN_H, SCREEN_W, RAIDER_PATROL_Y, RAIDER_PATROL_MS


def test_raider_empieza_en_bottom():
    r = Raider()
    assert r.rect.top >= SCREEN_H


def test_raider_estado_inicial_entering():
    r = Raider()
    assert r._state == "entering"


def test_raider_sube_durante_entering():
    r = Raider()
    y_inicial = r.y
    r.update(0.1)
    assert r.y < y_inicial  # subió


def test_raider_llega_a_patrol_y():
    r = Raider()
    # forzar posición justo encima del patrol_y para que transicione
    r.y = float(RAIDER_PATROL_Y + 1)
    r.rect.y = int(r.y)
    r.update(0.1)
    assert r._state == "patrolling"


def test_raider_patrol_timer_acumula():
    r = Raider()
    r._state = "patrolling"
    r.update(0.5)
    assert r._patrol_timer > 0


def test_raider_sale_tras_patrol_ms():
    r = Raider()
    r._state = "patrolling"
    r._patrol_timer = RAIDER_PATROL_MS - 10
    r.update(0.1)  # 100ms más → supera RAIDER_PATROL_MS
    assert r._state == "leaving"


def test_raider_no_dispara_durante_entering():
    r = Raider()
    now = pygame.time.get_ticks()
    shots = r.shoot(now)
    assert shots == []


def test_raider_no_dispara_durante_leaving():
    r = Raider()
    r._state = "leaving"
    now = pygame.time.get_ticks()
    shots = r.shoot(now)
    assert shots == []


def test_raider_dispara_durante_patrolling():
    from src.entities.enemy_bullet import EnemyBullet
    from src.settings import GUNNER_SHOOT_INTERVAL
    r = Raider()
    r._state = "patrolling"
    shots = r.shoot(GUNNER_SHOOT_INTERVAL)
    assert len(shots) == 3
    assert all(isinstance(b, EnemyBullet) for b in shots)


def test_raider_disparo_respeta_cooldown():
    from src.settings import GUNNER_SHOOT_INTERVAL
    r = Raider()
    r._state = "patrolling"
    r.shoot(GUNNER_SHOOT_INTERVAL)
    assert r.shoot(GUNNER_SHOOT_INTERVAL) == []


def test_raider_hp_inicial():
    from src.settings import RAIDER_HP
    r = Raider()
    assert r.hp == RAIDER_HP


def test_raider_puntos():
    from src.settings import RAIDER_POINTS
    r = Raider()
    assert r.points == RAIDER_POINTS


def test_raider_baja_en_leaving():
    r = Raider()
    r._state = "leaving"
    r.y = float(RAIDER_PATROL_Y)
    r.rect.y = int(r.y)
    y_inicial = r.y
    r.update(0.1)
    assert r.y > y_inicial


def test_raider_muere_al_tomar_dano_letal():
    from src.settings import RAIDER_HP
    r = Raider()
    r.take_damage(RAIDER_HP)
    assert not r.alive()
