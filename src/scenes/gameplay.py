import random
import pygame
from src.entities.player import Player
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.settings import (
    SCREEN_W, SCREEN_H, SCOUT_W, FIGHTER_W, SPAWN_INTERVAL,
    BULLET_DAMAGE, HUD_FONT_SIZE, HUD_COLOR, HUD_MARGIN,
)


class GameplayScene:
    def __init__(self):
        self._font = pygame.font.SysFont(None, HUD_FONT_SIZE)
        self.score = 0
        self.state = "start"
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.last_spawn = pygame.time.get_ticks()

    def _reset(self):
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.last_spawn = pygame.time.get_ticks()
        self.score = 0
        self.state = "playing"

    def process_input(self, events):
        keys = pygame.key.get_pressed()
        if self.state in ("start", "game_over"):
            if keys[pygame.K_SPACE]:
                self._reset()
            return
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
        if self.state != "playing":
            return

        self.player.update(dt)
        self.bullets.update(dt)
        self.enemies.update(dt)

        now = pygame.time.get_ticks()
        if now - self.last_spawn >= SPAWN_INTERVAL:
            self.last_spawn = now
            self.spawn_enemy()

        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in hit_enemies:
            self.score += enemy.points
            self.player.take_damage(now)

        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for enemies_hit in hits.values():
            for enemy in enemies_hit:
                if enemy.alive():
                    enemy.take_damage(BULLET_DAMAGE)
                    if not enemy.alive():
                        self.score += enemy.points

        if self.player.lives <= 0:
            self.state = "game_over"

    def _draw_overlay(self, screen, title, subtitle):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        title_surf = self._font.render(title, True, (255, 255, 255))
        sub_surf = self._font.render(subtitle, True, (180, 180, 180))
        cx = SCREEN_W // 2
        cy = SCREEN_H // 2
        screen.blit(title_surf, (cx - title_surf.get_width() // 2, cy - 30))
        screen.blit(sub_surf, (cx - sub_surf.get_width() // 2, cy + 10))

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)

        score_surf = self._font.render(f"SCORE: {self.score}", True, HUD_COLOR)
        screen.blit(score_surf, (HUD_MARGIN, HUD_MARGIN))

        lives_text = ("♥ " * self.player.lives).strip()
        lives_surf = self._font.render(lives_text, True, (220, 50, 50))
        screen.blit(lives_surf, (SCREEN_W - lives_surf.get_width() - HUD_MARGIN, HUD_MARGIN))

        if self.state == "start":
            self._draw_overlay(screen, "STARFALL", "PRESS SPACE TO PLAY")
        elif self.state == "game_over":
            self._draw_overlay(screen, "GAME OVER", "PRESS SPACE TO RESTART")
