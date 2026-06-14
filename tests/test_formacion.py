from unittest.mock import patch
from src.systems.spawning import SpawnSystem
from src.entities.scout import Scout
from src.settings import WAVE_FORMATION_MIN


def test_formacion_retorna_multiples_scouts():
    ss = SpawnSystem()
    scouts = ss._make_formation()
    assert len(scouts) >= 3
    assert len(scouts) <= 5
    for s in scouts:
        assert isinstance(s, Scout)


def test_formacion_solo_desde_wave_formation_min():
    ss = SpawnSystem()
    ss.wave = WAVE_FORMATION_MIN - 1
    # Con wave < WAVE_FORMATION_MIN, _make_spawn NO debe devolver formación
    # Forzar random.random() < 0.20 para asegurar que si hubiera formación, se dispararía
    with patch("src.systems.spawning.random.random", return_value=0.10):
        result = ss._make_spawn()
    assert len(result) == 1  # solo un enemigo


def test_formacion_disponible_desde_wave_formation_min():
    ss = SpawnSystem()
    ss.wave = WAVE_FORMATION_MIN
    with patch("src.systems.spawning.random.random", return_value=0.10):
        result = ss._make_spawn()
    assert len(result) >= 3  # formación


def test_formacion_cuenta_entre_3_y_5():
    ss = SpawnSystem()
    # Fijar randint para contar=4
    with patch("src.systems.spawning.random.randint", return_value=4):
        scouts = ss._make_formation()
    assert len(scouts) == 4


def test_formacion_todos_son_scouts():
    ss = SpawnSystem()
    scouts = ss._make_formation()
    assert all(isinstance(s, Scout) for s in scouts)


def test_formacion_scouts_tienen_speed_bonus():
    ss = SpawnSystem()
    ss.wave = WAVE_FORMATION_MIN
    from src.settings import WAVE_SPEED_FACTOR
    scouts = ss._make_formation()
    expected_bonus = ss.wave * WAVE_SPEED_FACTOR
    for s in scouts:
        assert s.speed_bonus == expected_bonus


def test_formacion_no_se_lanza_con_prob_alta():
    ss = SpawnSystem()
    ss.wave = WAVE_FORMATION_MIN
    # random.random() >= 0.20 → no se lanza formación
    with patch("src.systems.spawning.random.random", return_value=0.50):
        with patch("src.systems.spawning.random.randint", return_value=100):
            result = ss._make_spawn()
    assert len(result) == 1  # solo un enemigo (Scout al fallar todas las probs)
