import pygame
from src.scenes.gameplay import GameplayScene
from src.settings import COMBO_MULTIPLIERS, SHAKE_DURATION_MS


# --- v1.6: screen shake ---

def test_shake_activo_tras_hit():
    """_start_shake debe dejar _shake_ms > 0."""
    scene = GameplayScene()
    scene._start_shake(8)
    assert scene._shake_ms > 0


def test_shake_decrementa_con_tiempo():
    """Después de update(0.1), _shake_ms debe ser menor que el valor inicial."""
    scene = GameplayScene()
    scene._start_shake(8)
    initial = scene._shake_ms
    scene.update(0.1)   # 100 ms
    assert scene._shake_ms < initial


# --- v1.6: combo multiplier ---

def test_combo_get_multiplier_segun_nivel():
    """_get_multiplier() debe devolver el valor correcto para cada nivel de _combo."""
    scene = GameplayScene()

    # combo 0 → x1
    scene._combo = 0
    assert scene._get_multiplier() == COMBO_MULTIPLIERS[0]  # 1

    # combo 1 → x2
    scene._combo = 1
    assert scene._get_multiplier() == COMBO_MULTIPLIERS[1]  # 2

    # combo en el índice máximo (3) → x8
    max_idx = len(COMBO_MULTIPLIERS) - 1
    scene._combo = max_idx
    assert scene._get_multiplier() == COMBO_MULTIPLIERS[max_idx]  # 8

    # combo más allá del máximo → clampea al último valor
    scene._combo = max_idx + 99
    assert scene._get_multiplier() == COMBO_MULTIPLIERS[max_idx]  # 8


def test_combo_resetea_con_danio():
    """Al recibir daño real (player.lives baja), _combo y _combo_timer deben quedar en 0."""
    scene = GameplayScene()
    scene._combo = 2
    scene._combo_timer = 500.0
    # Asegurar que el jugador puede recibir daño (sin invincibilidad ni escudo)
    scene.player.invincible = False
    scene.player.active_powerups.discard("shield")
    scene.player.lives = 3   # vidas suficientes para no morir
    now = pygame.time.get_ticks()
    scene._handle_player_damage(now)
    assert scene._combo == 0
    assert scene._combo_timer == 0.0
