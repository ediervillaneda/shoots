import pygame
from src.entities.player import Player


class GameplayScene:
    def __init__(self):
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

    def process_input(self, events):
        keys = pygame.key.get_pressed()
        self.player.handle_keys(keys)
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot(pygame.time.get_ticks())
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

    def update(self, dt):
        self.player.update(dt)
        self.bullets.update(dt)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
