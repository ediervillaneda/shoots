import pygame
import src.assets as assets


def test_assets_get_returns_surface():
    surf = assets.get("powerups/shield.png")
    assert isinstance(surf, pygame.Surface)


def test_assets_get_cached():
    surf1 = assets.get("powerups/shield.png")
    surf2 = assets.get("powerups/shield.png")
    assert surf1 is surf2
