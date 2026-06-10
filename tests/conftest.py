import os
import pytest
import pygame

@pytest.fixture(autouse=True, scope="session")
def pygame_init():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture(autouse=True)
def clear_asset_cache():
    import src.assets as assets
    assets._cache.clear()
    yield
    assets._cache.clear()
