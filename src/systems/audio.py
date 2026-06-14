import pygame
from pathlib import Path

from src.settings.audio import MUSIC_VOLUME, SFX_VOLUME

_BASE = Path(__file__).parent.parent.parent / "assets"
_cache: dict[str, pygame.mixer.Sound] = {}
_muted: bool = False


def init() -> None:
    """Inicializar mixer. Llamar una vez desde Game.__init__."""
    if pygame.mixer.get_init():
        return
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    except pygame.error:
        pass


def play_sfx(path: str) -> None:
    if _muted or not pygame.mixer.get_init():
        return
    if path not in _cache:
        full = _BASE / path
        if not full.exists():
            return
        try:
            _cache[path] = pygame.mixer.Sound(str(full))
        except pygame.error:
            return
    _cache[path].set_volume(SFX_VOLUME)
    _cache[path].play()


def play_music(path: str) -> None:
    if not pygame.mixer.get_init():
        return
    full = _BASE / path
    if not full.exists():
        return
    try:
        pygame.mixer.music.load(str(full))
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


def stop_music() -> None:
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def toggle_mute() -> None:
    global _muted
    _muted = not _muted
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(0.0 if _muted else MUSIC_VOLUME)


def is_muted() -> bool:
    return _muted


def clear_cache() -> None:
    """Limpiar caché. Usar en tests."""
    _cache.clear()
