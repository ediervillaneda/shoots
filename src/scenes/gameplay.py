import math
import random
import pygame
import src.assets as assets
import src.systems.audio as audio
from src.entities.player import Player
from src.entities.scout import Scout
from src.entities.fighter import Fighter
from src.entities.kamikaze import Kamikaze
from src.entities.gunner import Gunner
from src.entities.striker import Striker
from src.entities.interceptor import Interceptor
from src.entities.orbiter import Orbiter
from src.entities.boss import Boss
from src.entities.powerup import PowerUp, POWERUP_ASSETS, POWERUP_KINDS
from src.entities.explosion import Explosion
from src.entities.impact_effect import ImpactEffect
from src.entities.laser import Laser
from src.entities.scrolling_bg import ScrollingBG
from src.systems.spawning import SpawnSystem
from src.settings import (
    SCREEN_W, SCREEN_H,
    HUD_FONT_SIZE, HUD_COLOR, HUD_MARGIN,
    POWERUP_DROP_CHANCE, PLAYER_W, PLAYER_H, SPRITE_HEART, SPRITE_SHIELD_OVERLAY,
    BOSS_HP, BOSS_HEALTH_BAR_H, BOSS_BAR_Y_OFFSET,
    ROCKET_DAMAGE, ROCKET_AREA_DAMAGE, ROCKET_RADIUS,
    EXPLOSION_W, EXPLOSION_H, EXPLOSION_W_BOSS, EXPLOSION_H_BOSS,
    EXPL_SCOUT, EXPL_KAMIKAZE, EXPL_FIGHTER,
    EXPL_GUNNER, EXPL_STRIKER, EXPL_INTERCEPTOR,
    EXPL_BOSS, EXPL_PLAYER,
    LASER_DAMAGE_PER_S,
    SHAKE_DURATION_MS, SHAKE_INTENSITY,
    COMBO_MULTIPLIERS, COMBO_TIMEOUT_MS,
    SHOT1_TRAVEL, SHOT2_TRAVEL, SHOT3_TRAVEL,
    SHOT4_TRAVEL, SHOT5_TRAVEL, SHOT6_TRAVEL,
)
from src.settings.audio import (
    MUSIC_GAMEPLAY,
    SFX_SHOOT, SFX_IMPACT, SFX_EXPLOSION,
    SFX_POWERUP, SFX_PLAYER_HIT, SFX_GAME_OVER, SFX_BOSS_HIT,
)


class GameplayScene:
    def __init__(self, game=None, mode: str = "endless"):
        self._game = game
        self._mode = mode
        self._time_left_ms: float = 0.0
        if mode == "daily":
            import random, datetime
            random.seed(datetime.date.today().toordinal())
        if mode == "survival":
            from src.settings import SURVIVAL_TIME_MS
            self._time_left_ms = float(SURVIVAL_TIME_MS)
        self._font = pygame.font.SysFont(None, HUD_FONT_SIZE)
        self.score = 0
        self.state = "playing"
        self._bg = ScrollingBG()
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self._laser_active: "Laser | None" = None
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_system = SpawnSystem()
        self.boss = None
        self._game_over_played = False
        self._shake_ms = 0.0
        self._shake_intensity = 0
        self._combo = 0
        self._combo_timer = 0.0
        audio.play_music(MUSIC_GAMEPLAY)

    def _reset(self):
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self._laser_active = None
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.spawn_system = SpawnSystem()
        self.state = "playing"
        self.boss = None
        self._game_over_played = False
        self._shake_ms = 0.0
        self._shake_intensity = 0
        self._combo = 0
        self._combo_timer = 0.0
        self._mode = getattr(self, "_mode", "endless")
        self._time_left_ms = 0.0
        if self._mode == "survival":
            from src.settings import SURVIVAL_TIME_MS
            self._time_left_ms = float(SURVIVAL_TIME_MS)

    def _start_shake(self, intensity: int) -> None:
        self._shake_ms = SHAKE_DURATION_MS
        self._shake_intensity = intensity

    def _get_multiplier(self) -> int:
        return COMBO_MULTIPLIERS[min(self._combo, len(COMBO_MULTIPLIERS) - 1)]

    def process_input(self, events):
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    audio.toggle_mute()
                elif event.key in (pygame.K_p, pygame.K_ESCAPE) and self.state == "playing":
                    self.state = "paused"
                elif self.state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        if self._game:
                            from src.scenes.menu import MenuScene
                            self._game.replace_scene(MenuScene(self._game))
                    elif event.key in (pygame.K_p, pygame.K_RETURN, pygame.K_SPACE):
                        self.state = "playing"
        if self.state == "game_over":
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self._reset()
            return
        if self.state == "paused":
            return
        self.player.handle_keys(keys)
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if "laser" in self.player.active_powerups:
                if self._laser_active is None or not self._laser_active.alive():
                    self._laser_active = Laser(self.player)
                    self.lasers.add(self._laser_active)
                    self.all_sprites.add(self._laser_active)
            bullets_fired = self.player.shoot(now)
            for bullet in bullets_fired:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
            if bullets_fired:
                audio.play_sfx(SFX_SHOOT)
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
            paths, size = EXPL_INTERCEPTOR, (EXPLOSION_W_BOSS,
                                             EXPLOSION_H_BOSS)
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
        audio.play_sfx(SFX_EXPLOSION)
        # v1.8: death_burst para Gunner y Striker
        if isinstance(entity, (Gunner, Striker)):
            for eb in entity.death_burst():
                self.enemy_bullets.add(eb)
                self.all_sprites.add(eb)

    def _handle_player_damage(self, now: int) -> None:
        lives_before = self.player.lives
        self.player.take_damage(now)
        if self.player.lives < lives_before:
            self._combo = 0
            self._combo_timer = 0.0
            expl = Explosion(
                self.player.rect.centerx, self.player.rect.centery, EXPL_PLAYER
            )
            self.explosions.add(expl)
            self.all_sprites.add(expl)
            audio.play_sfx(SFX_PLAYER_HIT)
            self._start_shake(SHAKE_INTENSITY)

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
                    self.score += enemy.points * self._get_multiplier()
                    self._combo = min(self._combo + 1, len(COMBO_MULTIPLIERS) - 1)
                    self._combo_timer = 0.0
                    self.spawn_system.register_kill()
                    self._maybe_drop_powerup(
                        enemy.rect.centerx, enemy.rect.centery)

    def update(self, dt):
        self._bg.update(dt)
        self._shake_ms = max(0.0, self._shake_ms - dt * 1000)
        if self.state != "playing":
            return

        self._combo_timer += dt * 1000
        if self._combo_timer > COMBO_TIMEOUT_MS:
            self._combo = 0
            self._combo_timer = 0.0

        if self._mode == "survival":
            self._time_left_ms -= dt * 1000
            if self._time_left_ms <= 0:
                self._time_left_ms = 0.0
                if not self._game_over_played:
                    self._game_over_played = True
                    audio.play_sfx(SFX_GAME_OVER)
                    if self._game:
                        from src.scenes.game_over import GameOverScene
                        self._game.replace_scene(GameOverScene(self._game, self.score))
                    else:
                        self.state = "game_over"

        self.player.update(dt)
        self.bullets.update(dt)
        self.rockets.update(dt)
        self.explosions.update(dt)
        self.lasers.update(dt)
        if self._laser_active and self._laser_active.alive():
            for enemy in list(self.enemies):
                if pygame.sprite.collide_rect(self._laser_active, enemy):
                    enemy.take_damage(LASER_DAMAGE_PER_S * dt)
                    if not enemy.alive():
                        self._spawn_death_explosion(enemy)
                        self.score += enemy.points * self._get_multiplier()
                        self._combo = min(self._combo + 1, len(COMBO_MULTIPLIERS) - 1)
                        self._combo_timer = 0.0
                        self.spawn_system.register_kill()
                        self._maybe_drop_powerup(
                            enemy.rect.centerx, enemy.rect.centery)
        self.enemies.update(dt)
        self.enemy_bullets.update(dt)
        self.powerups.update(dt)

        now = pygame.time.get_ticks()

        for enemy in self.spawn_system.update(now):
            if isinstance(enemy, (Kamikaze, Striker, Interceptor, Orbiter)):
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
            self._start_shake(SHAKE_INTENSITY * 2)
            self.spawn_system.notify_boss_killed()
            self.boss = None

        for sprite in self.enemies:
            if hasattr(sprite, "shoot"):
                for eb in sprite.shoot(now):
                    self.enemy_bullets.add(eb)
                    self.all_sprites.add(eb)

        eb_hits = pygame.sprite.spritecollide(
            self.player, self.enemy_bullets, True)
        for _ in eb_hits:
            self._handle_player_damage(now)

        hit_enemies = pygame.sprite.spritecollide(
            self.player, self.enemies, True)
        for enemy in hit_enemies:
            self._spawn_death_explosion(enemy)
            self.score += enemy.points * self._get_multiplier()
            self._combo = min(self._combo + 1, len(COMBO_MULTIPLIERS) - 1)
            self._combo_timer = 0.0
            self._handle_player_damage(now)
            self.spawn_system.register_kill()
            self._maybe_drop_powerup(enemy.rect.centerx, enemy.rect.centery)

        hits = pygame.sprite.groupcollide(
            self.bullets, self.enemies, True, False)
        for bullet, enemies_hit in hits.items():
            impact = ImpactEffect(
                bullet.rect.centerx, bullet.rect.centery,
                bullet.impact_frames, bullet.w, bullet.h,
            )
            self.explosions.add(impact)
            self.all_sprites.add(impact)
            audio.play_sfx(SFX_IMPACT)
            for enemy in enemies_hit:
                if enemy.alive():
                    is_boss = isinstance(enemy, Boss)
                    enemy.take_damage(bullet.damage)
                    if not enemy.alive():
                        self._spawn_death_explosion(enemy)
                        self.score += enemy.points * self._get_multiplier()
                        self._combo = min(self._combo + 1, len(COMBO_MULTIPLIERS) - 1)
                        self._combo_timer = 0.0
                        self.spawn_system.register_kill()
                        self._maybe_drop_powerup(
                            enemy.rect.centerx, enemy.rect.centery)
                    elif is_boss:
                        audio.play_sfx(SFX_BOSS_HIT)

        for rocket in list(self.rockets):
            hit = pygame.sprite.spritecollide(rocket, self.enemies, False)
            if hit:
                cx, cy = rocket.rect.center
                rocket.kill()
                self._explode(cx, cy, hit)

        picked = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for pu in picked:
            self.player.apply_powerup(pu.kind)
            audio.play_sfx(SFX_POWERUP)

        if self.player.lives <= 0:
            if not self._game_over_played:
                audio.play_sfx(SFX_GAME_OVER)
                self._game_over_played = True
                if self._game:
                    from src.scenes.game_over import GameOverScene
                    self._game.replace_scene(GameOverScene(self._game, self.score))
                else:
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
        if self._shake_ms > 0:
            _surf = pygame.Surface(screen.get_size())
        else:
            _surf = screen

        self._bg.draw(_surf)
        if not self.player.invincible:
            _surf.blit(self.player.shadow_image, self.player.shadow_rect)
        self.all_sprites.draw(_surf)

        score_surf = self._font.render(f"SCORE: {self.score}", True, HUD_COLOR)
        _surf.blit(score_surf, (HUD_MARGIN, HUD_MARGIN))

        mult = self._get_multiplier()
        if mult > 1:
            combo_surf = self._font.render(f"x{mult}", True, (255, 220, 0))
            _surf.blit(combo_surf, (HUD_MARGIN, HUD_MARGIN + HUD_FONT_SIZE + 4))

        wave_surf = self._font.render(
            f"WAVE: {self.spawn_system.wave}", True, HUD_COLOR)
        _surf.blit(wave_surf, (SCREEN_W // 2 -
                    wave_surf.get_width() // 2, HUD_MARGIN))

        if self._mode == "survival" and self._time_left_ms > 0:
            secs = int(self._time_left_ms / 1000)
            timer_surf = self._font.render(f"{secs // 60}:{secs % 60:02d}", True, (255, 100, 100))
            _surf.blit(timer_surf, (SCREEN_W - timer_surf.get_width() - HUD_MARGIN, HUD_MARGIN))
        elif self._mode == "daily":
            label = self._font.render("DAILY", True, (100, 200, 255))
            _surf.blit(label, (SCREEN_W - label.get_width() - HUD_MARGIN, HUD_MARGIN))

        heart = pygame.transform.scale(assets.get(SPRITE_HEART), (20, 20))
        for i in range(self.player.lives):
            _surf.blit(heart, (SCREEN_W - (i + 1) *
                        26 - HUD_MARGIN, HUD_MARGIN))

        if self.player.shield_level > 0:
            bonus = (0, 20, 36, 52)[self.player.shield_level]
            sh = assets.get(SPRITE_SHIELD_OVERLAY)
            sh_w = PLAYER_W + bonus
            sh_h = PLAYER_H + bonus
            sh_scaled = pygame.transform.scale(sh, (sh_w, sh_h))
            _surf.blit(sh_scaled, (
                self.player.rect.centerx - sh_w // 2,
                self.player.rect.top - sh_h,
            ))

        x = HUD_MARGIN
        for kind in sorted(self.player.active_powerups):
            icon = pygame.transform.scale(
                assets.get(POWERUP_ASSETS[kind]), (24, 24))
            _surf.blit(icon, (x, SCREEN_H - 24 - HUD_MARGIN))
            x += 28
        if self.player.rocket_count > 0:
            rocket_icon = pygame.transform.scale(
                assets.get(POWERUP_ASSETS["rocket"]), (24, 24))
            for _ in range(self.player.rocket_count):
                _surf.blit(rocket_icon, (x, SCREEN_H - 24 - HUD_MARGIN))
                x += 28

        if self.boss and self.boss.alive():
            bar_w = SCREEN_W - 2 * HUD_MARGIN
            filled = int(bar_w * self.boss.hp / BOSS_HP)
            y = HUD_MARGIN + HUD_FONT_SIZE + BOSS_BAR_Y_OFFSET
            pygame.draw.rect(_surf, (80, 0, 0),
                             (HUD_MARGIN, y, bar_w, BOSS_HEALTH_BAR_H))
            pygame.draw.rect(_surf, (220, 30, 30),
                             (HUD_MARGIN, y, filled, BOSS_HEALTH_BAR_H))
            pygame.draw.rect(_surf, (255, 255, 255),
                             (HUD_MARGIN, y, bar_w, BOSS_HEALTH_BAR_H), 1)

        # Icono nivel de armamento — centro inferior
        _SHOT_TRAVELS = (None, SHOT1_TRAVEL, SHOT2_TRAVEL, SHOT3_TRAVEL,
                         SHOT4_TRAVEL, SHOT5_TRAVEL, SHOT6_TRAVEL)
        travel = _SHOT_TRAVELS[self.player.shot_level]
        gun_icon = pygame.transform.scale(assets.get(travel[0]), (36, 36))
        _surf.blit(gun_icon, (SCREEN_W // 2 - 18, SCREEN_H - 36 - HUD_MARGIN))

        if self.state == "paused":
            self._draw_overlay(_surf, "PAUSED", "P/ENTER/SPACE: RESUME  ESC: MENU")
        elif self.state == "game_over":
            self._draw_overlay(_surf, "GAME OVER", "PRESS SPACE TO RESTART")

        if self._shake_ms > 0:
            ox = random.randint(-self._shake_intensity, self._shake_intensity)
            oy = random.randint(-self._shake_intensity, self._shake_intensity)
            screen.fill((0, 0, 0))
            screen.blit(_surf, (ox, oy))
