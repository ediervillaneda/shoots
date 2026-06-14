import pytest
import pygame
from unittest.mock import MagicMock


@pytest.fixture
def mock_game():
    game = MagicMock()
    return game


def test_menu_scene_instancia_sin_crash(mock_game):
    from src.scenes.menu import MenuScene
    scene = MenuScene(mock_game)
    assert scene._selected == 0


def test_menu_navegacion_down(mock_game):
    from src.scenes.menu import MenuScene
    scene = MenuScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, unicode="")
    scene.process_input([event])
    assert scene._selected == 1


def test_menu_navegacion_up_cicla(mock_game):
    from src.scenes.menu import MenuScene
    scene = MenuScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, unicode="")
    scene.process_input([event])
    assert scene._selected == 2  # cicla al último


def test_menu_esc_llama_pop_scene(mock_game):
    from src.scenes.menu import MenuScene
    scene = MenuScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, unicode="")
    scene.process_input([event])
    mock_game.pop_scene.assert_called_once()
