import sys
import pygame
from pathlib import Path


def _base_dir() -> Path:
    # sys._MEIPASS is set by PyInstaller at runtime
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).parent.parent


_BASE = _base_dir() / "assets"
_cache: dict[str, pygame.Surface] = {}


def get(path: str) -> pygame.Surface:
    if path not in _cache:
        _cache[path] = pygame.image.load(_BASE / path).convert_alpha()
    return _cache[path]
