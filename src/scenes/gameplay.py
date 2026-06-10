import pygame
from src.entities.player import Player
from src.entities.fighter import Fighter
from src.systems.spawning import SpawnSystem
from src.settings import (
    SCREEN_W, SCREEN_H,
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
        self.enemy_bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_system = SpawnSystem()

    def _reset(self):
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.spawn_system = SpawnSystem()
        self.state = "playing"

    def process_input(self, events):
        keys = pygame.key.get_pressed()
        if self.state in ("start", "game_over"):
            if keys[pygame.K_SPACE]:
                self._reset()
            return
        self.player.handle_keys(keys)
        if keys[pygame.K_SPACE]:
            for bullet in self.player.shoot(pygame.time.get_ticks()):
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

    def update(self, dt):
        if self.state != "playing":
            return

        self.player.update(dt)
        self.bullets.update(dt)
        self.enemies.update(dt)
        self.enemy_bullets.update(dt)

        now = pygame.time.get_ticks()

        for enemy in self.spawn_system.update(now):
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        for sprite in self.enemies:
            if isinstance(sprite, Fighter):
                eb = sprite.shoot(now)
                if eb:
                    self.enemy_bullets.add(eb)
                    self.all_sprites.add(eb)

        eb_hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for _ in eb_hits:
            self.player.take_damage(now)

        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in hit_enemies:
            self.score += enemy.points
            self.player.take_damage(now)
            self.spawn_system.register_kill()

        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for enemies_hit in hits.values():
            for enemy in enemies_hit:
                if enemy.alive():
                    enemy.take_damage(BULLET_DAMAGE)
                    if not enemy.alive():
                        self.score += enemy.points
                        self.spawn_system.register_kill()

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

        wave_surf = self._font.render(f"WAVE: {self.spawn_system.wave}", True, HUD_COLOR)
        screen.blit(wave_surf, (SCREEN_W // 2 - wave_surf.get_width() // 2, HUD_MARGIN))

        lives_text = ("♥ " * self.player.lives).strip()
        lives_surf = self._font.render(lives_text, True, (220, 50, 50))
        screen.blit(lives_surf, (SCREEN_W - lives_surf.get_width() - HUD_MARGIN, HUD_MARGIN))

        if self.state == "start":
            self._draw_overlay(screen, "STARFALL", "PRESS SPACE TO PLAY")
        elif self.state == "game_over":
            self._draw_overlay(screen, "GAME OVER", "PRESS SPACE TO RESTART")
