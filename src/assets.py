import pygame
from pathlib import Path

_BASE = Path(__file__).parent.parent / "assets"
_cache: dict[str, pygame.Surface] = {}


def get(path: str) -> pygame.Surface:
    if path not in _cache:
        _cache[path] = pygame.image.load(_BASE / path).convert_alpha()
    return _cache[path]
