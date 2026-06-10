import random
import pygame
from src.entities.player import Player
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.settings import SCREEN_W, SCOUT_W, FIGHTER_W, SPAWN_INTERVAL, BULLET_DAMAGE


class GameplayScene:
    def __init__(self):
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.last_spawn = pygame.time.get_ticks()

    def process_input(self, events):
        keys = pygame.key.get_pressed()
        self.player.handle_keys(keys)
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot(pygame.time.get_ticks())
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

    def spawn_enemy(self):
        cls = random.choice([Scout, Fighter])
        margin = max(SCOUT_W, FIGHTER_W) // 2
        x = random.randint(margin, SCREEN_W - margin)
        enemy = cls(x)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def update(self, dt):
        self.player.update(dt)
        self.bullets.update(dt)
        self.enemies.update(dt)

        now = pygame.time.get_ticks()
        if now - self.last_spawn >= SPAWN_INTERVAL:
            self.last_spawn = now
            self.spawn_enemy()

        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for enemies_hit in hits.values():
            for enemy in enemies_hit:
                enemy.take_damage(BULLET_DAMAGE)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
