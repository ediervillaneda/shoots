import pygame
from src.entities.flanker import Flanker
from src.settings import SCREEN_W, FLANKER_W, FLANKER_CROSS_Y


def test_flanker_empieza_fuera_pantalla_izquierda():
    f = Flanker(from_left=True)
    assert f.rect.right <= 0  # empieza a la izquierda


def test_flanker_empieza_fuera_pantalla_derecha():
    f = Flanker(from_left=False)
    assert f.rect.left >= SCREEN_W  # empieza a la derecha


def test_flanker_centery_es_cross_y():
    f = Flanker(from_left=True)
    assert f.rect.centery == FLANKER_CROSS_Y


def test_flanker_estado_inicial_crossing():
    f = Flanker(from_left=True)
    assert f._state == "crossing"


def test_flanker_target_x_en_rango():
    for _ in range(20):
        f = Flanker(from_left=True)
        assert SCREEN_W // 4 <= f._target_x <= SCREEN_W * 3 // 4


def test_flanker_cruza_y_cambia_a_descending():
    f = Flanker(from_left=True)
    # forzar target_x cercano para que la transición ocurra rápido
    f._target_x = f.x + 10
    f.update(1.0)  # dt grande
    assert f._state == "descending"


def test_flanker_se_mueve_derecha_desde_izquierda():
    f = Flanker(from_left=True)
    x_inicial = f.x
    f.update(0.05)
    assert f.x > x_inicial


def test_flanker_se_mueve_izquierda_desde_derecha():
    f = Flanker(from_left=False)
    x_inicial = f.x
    f.update(0.05)
    assert f.x < x_inicial


def test_flanker_hp_inicial():
    from src.settings import FLANKER_HP
    f = Flanker(from_left=True)
    assert f.hp == FLANKER_HP


def test_flanker_puntos():
    from src.settings import FLANKER_POINTS
    f = Flanker(from_left=True)
    assert f.points == FLANKER_POINTS


def test_flanker_descending_baja():
    f = Flanker(from_left=True)
    f._state = "descending"
    y_inicial = f.y
    f.update(0.1)
    assert f.y > y_inicial


def test_flanker_muere_al_tomar_dano_letal():
    from src.settings import FLANKER_HP
    f = Flanker(from_left=True)
    f.take_damage(FLANKER_HP)
    assert not f.alive()
