import math
import pygame
from src.entities.player import Player, calc_velocity
from src.settings import SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H, BULLET_COOLDOWN


def test_velocity_right():
    vx, vy = calc_velocity(left=False, right=True, up=False, down=False)
    assert vx == 1.0 and vy == 0.0

def test_velocity_left():
    vx, vy = calc_velocity(left=True, right=False, up=False, down=False)
    assert vx == -1.0 and vy == 0.0

def test_velocity_up():
    vx, vy = calc_velocity(left=False, right=False, up=True, down=False)
    assert vx == 0.0 and vy == -1.0

def test_velocity_diagonal_normalized():
    vx, vy = calc_velocity(left=False, right=True, up=True, down=False)
    magnitude = math.sqrt(vx**2 + vy**2)
    assert abs(magnitude - 1.0) < 0.001

def test_velocity_idle():
    vx, vy = calc_velocity(left=False, right=False, up=False, down=False)
    assert vx == 0.0 and vy == 0.0

def test_player_initial_position():
    player = Player()
    assert player.rect.centerx == SCREEN_W // 2
    assert player.rect.bottom == SCREEN_H - 80

def test_player_clamped_to_screen_right():
    player = Player()
    player.rect.x = SCREEN_W + 100
    player.x = float(player.rect.x)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.right <= SCREEN_W

def test_player_clamped_to_screen_left():
    player = Player()
    player.rect.x = -200
    player.x = float(player.rect.x)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.left >= 0

def test_player_shoot_returns_bullet():
    from src.entities.bullet import Bullet
    player = Player()
    bullets = player.shoot(BULLET_COOLDOWN + 1)
    assert len(bullets) == 1
    assert isinstance(bullets[0], Bullet)

def test_player_shoot_respects_cooldown():
    player = Player()
    player.last_shot = 1000
    assert player.shoot(1000 + BULLET_COOLDOWN - 1) == []

def test_player_bullet_spawns_at_player_top():
    from src.entities.bullet import Bullet
    player = Player()
    bullets = player.shoot(BULLET_COOLDOWN + 1)
    assert bullets[0].rect.centerx == player.rect.centerx
    assert bullets[0].rect.bottom == player.rect.top

def test_player_clamped_to_screen_bottom():
    player = Player()
    player.rect.y = SCREEN_H + 100
    player.y = float(player.rect.y)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.bottom <= SCREEN_H

def test_player_clamped_to_screen_top():
    player = Player()
    player.rect.y = -200
    player.y = float(player.rect.y)
    player.vel_x = 0.0
    player.vel_y = 0.0
    player.update(0.016)
    assert player.rect.top >= 0


# --- v0.3: lives & invincibility ---

def test_player_initial_lives():
    from src.settings import PLAYER_LIVES
    player = Player()
    assert player.lives == PLAYER_LIVES


def test_take_damage_reduces_lives():
    from src.settings import PLAYER_LIVES
    player = Player()
    player.take_damage(0)
    assert player.lives == PLAYER_LIVES - 1


def test_take_damage_activates_invincibility():
    player = Player()
    player.take_damage(0)
    assert player.invincible is True


def test_take_damage_ignored_when_invincible():
    from src.settings import PLAYER_LIVES
    player = Player()
    player.take_damage(0)   # primera vez: invincible=True
    player.take_damage(0)   # segunda vez: ignorada
    assert player.lives == PLAYER_LIVES - 1


def test_invincibility_expires_after_update():
    player = Player()
    player.invincible = True
    player.invincible_until = 0   # ya expiró (pygame.time.get_ticks() > 0)
    player.update(0.016)
    assert player.invincible is False


def test_invincibility_not_expired_if_future():
    player = Player()
    player.invincible = True
    player.invincible_until = pygame.time.get_ticks() + 10_000
    player.update(0.016)
    assert player.invincible is True


# --- v0.5: active_powerups ---

def test_player_no_active_powerups_on_init():
    player = Player()
    assert player.active_powerups == set()


def test_apply_powerup_adds_to_set():
    player = Player()
    player.apply_powerup("shield")
    assert player.shield_level == 1


def test_apply_powerup_rapid_fire():
    player = Player()
    player.apply_powerup("rapid_fire")
    assert "rapid_fire" in player.active_powerups


def test_player_initial_shot_level():
    player = Player()
    assert player.shot_level == 1


def test_gun_upgrade_increments_to_double():
    player = Player()
    player.apply_powerup("gun_upgrade")
    assert player.shot_level == 2


def test_gun_upgrade_twice_increments_to_triple():
    player = Player()
    player.apply_powerup("gun_upgrade")
    player.apply_powerup("gun_upgrade")
    assert player.shot_level == 3


def test_gun_upgrade_capped_at_triple():
    from src.settings import SHOT_LEVEL_MAX
    player = Player()
    for _ in range(10):
        player.apply_powerup("gun_upgrade")
    assert player.shot_level == SHOT_LEVEL_MAX


def test_apply_powerup_extra_life_increments_lives():
    from src.settings import PLAYER_LIVES, PLAYER_LIVES_MAX
    player = Player()
    player.apply_powerup("extra_life")
    assert player.lives == PLAYER_LIVES + 1


def test_apply_powerup_extra_life_capped_at_max():
    from src.settings import PLAYER_LIVES_MAX
    player = Player()
    player.lives = PLAYER_LIVES_MAX
    player.apply_powerup("extra_life")
    assert player.lives == PLAYER_LIVES_MAX


def test_apply_powerup_extra_life_not_in_set():
    player = Player()
    player.apply_powerup("extra_life")
    assert "extra_life" not in player.active_powerups


# --- v0.5: shoot() returns list ---

def test_shoot_returns_list():
    player = Player()
    result = player.shoot(0)
    assert isinstance(result, list)


def test_shoot_returns_one_bullet_normally():
    from src.entities.bullet import Bullet
    player = Player()
    bullets = player.shoot(0)
    assert len(bullets) == 1
    assert isinstance(bullets[0], Bullet)


def test_shoot_returns_empty_list_on_cooldown():
    player = Player()
    player.shoot(0)
    assert player.shoot(0) == []


def test_shoot_gun_upgrade_once_returns_two_bullets():
    player = Player()
    player.apply_powerup("gun_upgrade")
    bullets = player.shoot(0)
    assert len(bullets) == 2


def test_shoot_gun_upgrade_twice_returns_three_bullets():
    player = Player()
    player.apply_powerup("gun_upgrade")
    player.apply_powerup("gun_upgrade")
    bullets = player.shoot(0)
    assert len(bullets) == 3


def test_shoot_rapidfire_allows_shoot_at_reduced_cooldown():
    from src.settings import BULLET_COOLDOWN, RAPIDFIRE_COOLDOWN_MULT
    player = Player()
    player.apply_powerup("rapid_fire")
    player.shoot(0)
    reduced = int(BULLET_COOLDOWN * RAPIDFIRE_COOLDOWN_MULT)
    bullets = player.shoot(reduced)
    assert len(bullets) == 1


# --- v0.5: take_damage with shield ---

def test_take_damage_shield_absorbs_hit():
    from src.settings import PLAYER_LIVES
    player = Player()
    player.apply_powerup("shield")
    player.take_damage(0)
    assert player.lives == PLAYER_LIVES


def test_take_damage_shield_removed_after_absorb():
    player = Player()
    player.apply_powerup("shield")
    player.take_damage(0)
    assert "shield" not in player.active_powerups


def test_take_damage_shield_preserves_other_powerups():
    player = Player()
    player.apply_powerup("shield")
    player.apply_powerup("rapid_fire")
    player.take_damage(0)
    assert "rapid_fire" in player.active_powerups


def test_take_damage_clears_active_powerups():
    player = Player()
    player.apply_powerup("rapid_fire")
    player.apply_powerup("shield")
    player.take_damage(0)  # shield absorbs, no damage
    player.take_damage(0)  # second hit: real damage clears powerups
    assert player.active_powerups == set()


def test_take_damage_resets_shot_level():
    player = Player()
    player.apply_powerup("gun_upgrade")
    player.apply_powerup("gun_upgrade")
    assert player.shot_level == 3
    player.take_damage(0)
    assert player.shot_level == 1


# --- v0.7: rocket powerup ---

def test_shoot_rocket_without_powerup_returns_empty():
    from src.entities.rocket import Rocket
    player = Player()
    assert player.shoot_rocket(0) == []


def test_shoot_rocket_with_powerup_returns_rocket():
    from src.entities.rocket import Rocket
    from src.settings import ROCKET_COOLDOWN
    player = Player()
    player.apply_powerup("rocket")
    rockets = player.shoot_rocket(ROCKET_COOLDOWN)
    assert len(rockets) == 1
    assert isinstance(rockets[0], Rocket)


def test_shoot_rocket_respects_cooldown():
    from src.settings import ROCKET_COOLDOWN
    player = Player()
    player.apply_powerup("rocket")
    player.shoot_rocket(ROCKET_COOLDOWN)
    assert player.shoot_rocket(ROCKET_COOLDOWN) == []


def test_shoot_rocket_spawns_at_left_side():
    from src.entities.rocket import Rocket
    from src.settings import ROCKET_COOLDOWN
    player = Player()
    player.apply_powerup("rocket")
    rockets = player.shoot_rocket(ROCKET_COOLDOWN)
    # left-side rocket: centerx at player.rect.left, bottom at player.rect.top
    assert rockets[0].rect.centerx == player.rect.left
    assert rockets[0].rect.bottom == player.rect.top


# --- v0.8: rocket_count, dual rockets, shot levels 4-6 ---

def test_rocket_count_starts_at_zero():
    player = Player()
    assert player.rocket_count == 0


def test_apply_rocket_increments_count():
    player = Player()
    player.apply_powerup("rocket")
    assert player.rocket_count == 1


def test_apply_rocket_twice_gives_count_two():
    player = Player()
    player.apply_powerup("rocket")
    player.apply_powerup("rocket")
    assert player.rocket_count == 2


def test_apply_rocket_capped_at_two():
    from src.settings import ROCKET_MAX_COUNT
    player = Player()
    for _ in range(5):
        player.apply_powerup("rocket")
    assert player.rocket_count == ROCKET_MAX_COUNT


def test_shoot_rocket_fires_two_when_count_two():
    from src.entities.rocket import Rocket
    from src.settings import ROCKET_COOLDOWN
    player = Player()
    player.apply_powerup("rocket")
    player.apply_powerup("rocket")
    rockets = player.shoot_rocket(ROCKET_COOLDOWN)
    assert len(rockets) == 2


def test_shoot_two_rockets_spawn_at_sides():
    from src.entities.rocket import Rocket
    from src.settings import ROCKET_COOLDOWN
    player = Player()
    player.apply_powerup("rocket")
    player.apply_powerup("rocket")
    rockets = player.shoot_rocket(ROCKET_COOLDOWN)
    assert rockets[0].rect.centerx == player.rect.left
    assert rockets[1].rect.centerx == player.rect.right


def test_take_damage_resets_rocket_count():
    player = Player()
    player.apply_powerup("rocket")
    player.apply_powerup("rocket")
    player.take_damage(0)
    assert player.rocket_count == 0


def test_rocket_not_in_active_powerups():
    player = Player()
    player.apply_powerup("rocket")
    assert "rocket" not in player.active_powerups


def test_shot_level_max_is_six():
    from src.settings import SHOT_LEVEL_MAX
    assert SHOT_LEVEL_MAX == 6


def test_gun_upgrade_to_level_four():
    player = Player()
    for _ in range(3):
        player.apply_powerup("gun_upgrade")
    assert player.shot_level == 4


def test_shoot_level_four_returns_three_bullets():
    player = Player()
    for _ in range(3):
        player.apply_powerup("gun_upgrade")
    bullets = player.shoot(0)
    assert len(bullets) == 3


def test_shoot_level_five_returns_five_bullets():
    player = Player()
    for _ in range(4):
        player.apply_powerup("gun_upgrade")
    bullets = player.shoot(0)
    assert len(bullets) == 5


def test_shoot_level_six_returns_five_bullets():
    player = Player()
    for _ in range(5):
        player.apply_powerup("gun_upgrade")
    bullets = player.shoot(0)
    assert len(bullets) == 5


# --- v1.4: gun_upgrade divergencia lateral + tint por powerup activo ---

def test_gun_upgrade_lvl2_balas_divergen():
    p = Player()
    p.shot_level = 2
    balas = p.shoot(0)
    assert len(balas) == 2
    assert balas[0]._vx < 0   # izquierda va hacia la izq
    assert balas[1]._vx > 0   # derecha va hacia la der


def test_gun_upgrade_lvl3_balas_divergen():
    p = Player()
    p.shot_level = 3
    balas = p.shoot(0)
    assert len(balas) == 3
    assert balas[0]._vx < 0
    assert abs(balas[1]._vx) < 0.001   # centro recto
    assert balas[2]._vx > 0


def test_gun_upgrade_lvl5_balas_divergen():
    p = Player()
    p.shot_level = 5
    balas = p.shoot(0)
    assert len(balas) == 5
    assert balas[0]._vx < balas[1]._vx < 0   # -2x < -1x < 0
    assert abs(balas[2]._vx) < 0.001
    assert balas[3]._vx > 0
    assert balas[4]._vx > balas[3]._vx   # +2x > +1x


def test_shield_activo_tint_en_balas():
    from src.settings import BULLET_TINT_SHIELD
    p = Player()
    p.shield_level = 1
    balas = p.shoot(0)
    assert balas[0].tint == BULLET_TINT_SHIELD


def test_rapidfire_activo_damage_reducido():
    from src.settings import BULLET_DAMAGE_DEFAULT
    p = Player()
    p.active_powerups.add("rapid_fire")
    p.last_shot = -9999
    balas = p.shoot(0)
    expected = max(1, int(BULLET_DAMAGE_DEFAULT * 0.5))
    assert balas[0].damage == expected


def test_ambos_powerups_no_crash():
    p = Player()
    p.active_powerups.add("rapid_fire")
    p.active_powerups.add("shield")
    p.last_shot = -9999
    balas = p.shoot(0)
    assert len(balas) >= 1


def test_spread_dispara_5_balas():
    p = Player()
    p.active_powerups.add("spread")
    balas = p.shoot(0)
    assert len(balas) == 5


def test_spread_balas_tienen_angulos_distintos():
    p = Player()
    p.active_powerups.add("spread")
    balas = p.shoot(0)
    vx_values = [b._vx for b in balas]
    assert len(set(round(v, 4) for v in vx_values)) == 5


def test_plasma_dispara_1_bala_danio_alto():
    from src.settings import PLASMA_DAMAGE
    p = Player()
    p.active_powerups.add("plasma")
    balas = p.shoot(0)
    assert len(balas) == 1
    assert balas[0].damage == PLASMA_DAMAGE
