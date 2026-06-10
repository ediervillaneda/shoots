import pygame
from src.entities.explosion import Explosion
from src.settings import EXPLOSION_W, EXPLOSION_H, EXPLOSION_FRAME_MS, EXPLOSION_FRAMES


def test_explosion_spawns_at_position():
    expl = Explosion(270, 400)
    assert expl.rect.center == (270, 400)


def test_explosion_image_size():
    expl = Explosion(270, 400)
    assert expl.image.get_size() == (EXPLOSION_W, EXPLOSION_H)


def test_explosion_starts_on_first_frame():
    expl = Explosion(270, 400)
    assert expl._frame == 0


def test_explosion_advances_frame_after_interval():
    expl = Explosion(270, 400)
    expl.update(EXPLOSION_FRAME_MS / 1000)
    assert expl._frame == 1


def test_explosion_does_not_advance_before_interval():
    expl = Explosion(270, 400)
    expl.update((EXPLOSION_FRAME_MS - 1) / 1000)
    assert expl._frame == 0


def test_explosion_kills_itself_after_all_frames():
    expl = Explosion(270, 400)
    group = pygame.sprite.Group(expl)
    total_ms = EXPLOSION_FRAME_MS * len(EXPLOSION_FRAMES)
    expl.update(total_ms / 1000)
    assert not expl.alive()
