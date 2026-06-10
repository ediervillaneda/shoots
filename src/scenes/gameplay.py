import math
import random
import pygame
import src.assets as assets
from src.entities.player import Player
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.kamikaze import Kamikaze
from src.entities.gunner import Gunner
from src.entities.striker import Striker
from src.entities.interceptor import Interceptor
from src.entities.boss import Boss
from src.entities.powerup import PowerUp, POWERUP_ASSETS, POWERUP_KINDS
from src.entities.explosion import Explosion
from src.systems.spawning import SpawnSystem
from src.settings import (
    SCREEN_W, SCREEN_H,
    BULLET_DAMAGE, HUD_FONT_SIZE, HUD_COLOR, HUD_MARGIN,
    POWERUP_DROP_CHANCE, PLAYER_W, PLAYER_H, SPRITE_SHIELD_OVERLAY,
    BOSS_HP, BOSS_HEALTH_BAR_H, BOSS_BAR_Y_OFFSET,
    ROCKET_DAMAGE, ROCKET_AREA_DAMAGE, ROCKET_RADIUS,
    EXPLOSION_W, EXPLOSION_H, EXPLOSION_W_BOSS, EXPLOSION_H_BOSS,
    EXPL_SCOUT, EXPL_KAMIKAZE, EXPL_FIGHTER,
    EXPL_GUNNER, EXPL_STRIKER, EXPL_INTERCEPTOR,
    EXPL_BOSS, EXPL_PLAYER,
)


class GameplayScene:
    def __init__(self):
        self._font = pygame.font.SysFont(None, HUD_FONT_SIZE)
        self.score = 0
        self.state = "start"
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_system = SpawnSystem()
        self.boss = None

    def _reset(self):
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.spawn_system = SpawnSystem()
        self.state = "playing"
        self.boss = None

    def process_input(self, events):
        keys = pygame.key.get_pressed()
        if self.state in ("start", "game_over"):
            if keys[pygame.K_SPACE]:
                self._reset()
            return
        self.player.handle_keys(keys)
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            for bullet in self.player.shoot(now):
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
            for rocket in self.player.shoot_rocket(now):
                self.rockets.add(rocket)
                self.all_sprites.add(rocket)

    def _maybe_drop_powerup(self, x, y):
        if random.random() < POWERUP_DROP_CHANCE:
            kind = random.choice(POWERUP_KINDS)
            pu = PowerUp(kind, x, y)
            self.powerups.add(pu)
            self.all_sprites.add(pu)

    def _spawn_death_explosion(self, entity) -> None:
        if isinstance(entity, Boss):
            paths, size = EXPL_BOSS, (EXPLOSION_W_BOSS, EXPLOSION_H_BOSS)
        elif isinstance(entity, Interceptor):
            paths, size = EXPL_INTERCEPTOR, (EXPLOSION_W_BOSS, EXPLOSION_H_BOSS)
        elif isinstance(entity, Striker):
            paths, size = EXPL_STRIKER, (EXPLOSION_W, EXPLOSION_H)
        elif isinstance(entity, Gunner):
            paths, size = EXPL_GUNNER, (EXPLOSION_W, EXPLOSION_H)
        elif isinstance(entity, Fighter):
            paths, size = EXPL_FIGHTER, (EXPLOSION_W, EXPLOSION_H)
        elif isinstance(entity, Kamikaze):
            paths, size = EXPL_KAMIKAZE, (EXPLOSION_W, EXPLOSION_H)
        else:
            paths, size = EXPL_SCOUT, (EXPLOSION_W, EXPLOSION_H)
        expl = Explosion(entity.rect.centerx, entity.rect.centery, paths, size)
        self.explosions.add(expl)
        self.all_sprites.add(expl)

    def _handle_player_damage(self, now: int) -> None:
        lives_before = self.player.lives
        self.player.take_damage(now)
        if self.player.lives < lives_before:
            expl = Explosion(
                self.player.rect.centerx, self.player.rect.centery, EXPL_PLAYER
            )
            self.explosions.add(expl)
            self.all_sprites.add(expl)

    def _explode(self, cx: int, cy: int, direct_hits: list) -> None:
        expl = Explosion(cx, cy)
        self.explosions.add(expl)
        self.all_sprites.add(expl)
        direct_set = set(direct_hits)
        for enemy in list(self.enemies):
            if not enemy.alive():
                continue
            dist = math.hypot(enemy.rect.centerx - cx, enemy.rect.centery - cy)
            dmg = ROCKET_DAMAGE if enemy in direct_set else ROCKET_AREA_DAMAGE
            if enemy in direct_set or dist <= ROCKET_RADIUS:
                enemy.take_damage(dmg)
                if not enemy.alive():
                    self._spawn_death_explosion(enemy)
                    self.score += enemy.points
                    self.spawn_system.register_kill()
                    self._maybe_drop_powerup(enemy.rect.centerx, enemy.rect.centery)

    def update(self, dt):
        if self.state != "playing":
            return

        self.player.update(dt)
        self.bullets.update(dt)
        self.rockets.update(dt)
        self.explosions.update(dt)
        self.enemies.update(dt)
        self.enemy_bullets.update(dt)
        self.powerups.update(dt)

        now = pygame.time.get_ticks()

        for enemy in self.spawn_system.update(now):
            if isinstance(enemy, (Kamikaze, Striker, Interceptor)):
                enemy.target = self.player
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        b = self.spawn_system.get_boss_spawn()
        if b:
            self.boss = b
            self.enemies.add(b)
            self.all_sprites.add(b)

        if self.boss and self.boss.alive():
            for eb in self.boss.shoot(now):
                self.enemy_bullets.add(eb)
                self.all_sprites.add(eb)

        if self.boss and not self.boss.alive():
            self._spawn_death_explosion(self.boss)
            self.spawn_system.notify_boss_killed()
            self.boss = None

        for sprite in self.enemies:
            if hasattr(sprite, "shoot"):
                for eb in sprite.shoot(now):
                    self.enemy_bullets.add(eb)
                    self.all_sprites.add(eb)

        eb_hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for _ in eb_hits:
            self._handle_player_damage(now)

        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in hit_enemies:
            self._spawn_death_explosion(enemy)
            self.score += enemy.points
            self._handle_player_damage(now)
            self.spawn_system.register_kill()
            self._maybe_drop_powerup(enemy.rect.centerx, enemy.rect.centery)

        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for enemies_hit in hits.values():
            for enemy in enemies_hit:
                if enemy.alive():
                    enemy.take_damage(BULLET_DAMAGE)
                    if not enemy.alive():
                        self._spawn_death_explosion(enemy)
                        self.score += enemy.points
                        self.spawn_system.register_kill()
                        self._maybe_drop_powerup(enemy.rect.centerx, enemy.rect.centery)

        for rocket in list(self.rockets):
            hit = pygame.sprite.spritecollide(rocket, self.enemies, False)
            if hit:
                cx, cy = rocket.rect.center
                rocket.kill()
                self._explode(cx, cy, hit)

        picked = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for pu in picked:
            self.player.apply_powerup(pu.kind)

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

        if "shield" in self.player.active_powerups:
            sh = assets.get(SPRITE_SHIELD_OVERLAY)
            sh_scaled = pygame.transform.scale(sh, (PLAYER_W + 20, PLAYER_H + 20))
            screen.blit(sh_scaled, (
                self.player.rect.centerx - sh_scaled.get_width() // 2,
                self.player.rect.top - 10,
            ))

        x = HUD_MARGIN
        for kind in sorted(self.player.active_powerups):
            icon = pygame.transform.scale(assets.get(POWERUP_ASSETS[kind]), (24, 24))
            screen.blit(icon, (x, SCREEN_H - 24 - HUD_MARGIN))
            x += 28
        if self.player.rocket_count > 0:
            rocket_icon = pygame.transform.scale(assets.get(POWERUP_ASSETS["rocket"]), (24, 24))
            for _ in range(self.player.rocket_count):
                screen.blit(rocket_icon, (x, SCREEN_H - 24 - HUD_MARGIN))
                x += 28

        if self.boss and self.boss.alive():
            bar_w = SCREEN_W - 2 * HUD_MARGIN
            filled = int(bar_w * self.boss.hp / BOSS_HP)
            y = HUD_MARGIN + HUD_FONT_SIZE + BOSS_BAR_Y_OFFSET
            pygame.draw.rect(screen, (80, 0, 0),      (HUD_MARGIN, y, bar_w, BOSS_HEALTH_BAR_H))
            pygame.draw.rect(screen, (220, 30, 30),   (HUD_MARGIN, y, filled, BOSS_HEALTH_BAR_H))
            pygame.draw.rect(screen, (255, 255, 255), (HUD_MARGIN, y, bar_w, BOSS_HEALTH_BAR_H), 1)

        if self.state == "start":
            self._draw_overlay(screen, "STARFALL", "PRESS SPACE TO PLAY")
        elif self.state == "game_over":
            self._draw_overlay(screen, "GAME OVER", "PRESS SPACE TO RESTART")
