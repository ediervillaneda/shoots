import pytest
import pygame
from src.entities.laser import Laser
from src.entities.player import Player
from src.settings import LASER_DURATION_MS, LASER_DAMAGE_PER_S, LASER_W


def test_laser_sigue_al_player():
    p = Player()
    laser = Laser(p)
    p.rect.centerx = 300
    laser.update(0.016)
    assert laser.rect.centerx == 300


def test_laser_se_destruye_tras_duracion():
    p = Player()
    laser = Laser(p)
    group = pygame.sprite.Group(laser)
    laser.update(LASER_DURATION_MS / 1000 + 0.1)
    group.update(0)
    assert not laser.alive()


def test_laser_descarta_powerup_al_morir():
    p = Player()
    p.active_powerups.add("laser")
    laser = Laser(p)
    laser.update(LASER_DURATION_MS / 1000 + 0.1)
    assert "laser" not in p.active_powerups


def test_laser_ancho_correcto():
    p = Player()
    laser = Laser(p)
    assert laser.rect.width == LASER_W
