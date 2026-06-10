import pygame
from src.settings import SCREEN_H


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, w, h, color, hp, points):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(centerx=x, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.hp = hp
        self.points = points

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

    def update(self, dt):
        if self.rect.top > SCREEN_H:
            self.kill()
