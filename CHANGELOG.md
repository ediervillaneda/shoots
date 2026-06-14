# Changelog

All notable changes to Starfall are documented here.

---

## [1.6.0] — Game feel: screen shake, combo multiplier, flash de daño

### 1.6.2
- `Enemy._base_image` capturado lazy en `take_damage()` (no en `__init__`) — fix: subclases actualizan `self.image` después del super().__init__; ahora el sprite real es el que se flashea
- `_combo_timer` se resetea a 0 tras timeout — fix: el combo podía reconstruirse correctamente tras la primera expiración
- `ENEMY_FLASH_ALPHA = 80` extraído a settings (sin magic number en entity)

### 1.6.1
- `src/settings/gameplay.py`: constantes `SHAKE_DURATION_MS`, `SHAKE_INTENSITY`, `COMBO_MULTIPLIERS`, `COMBO_TIMEOUT_MS`, `ENEMY_FLASH_MS`
- `Enemy.take_damage()`: activa `_flash_ms = ENEMY_FLASH_MS` al sobrevivir; `update()` tinta blanco 80ms con `BLEND_RGBA_ADD`
- `GameplayScene._start_shake()`: screen shake 400ms con offset random; se activa al perder vida y al matar boss (intensidad doble)
- `GameplayScene`: combo multiplier x1-x8 en score; reset tras 3s sin kills o al recibir daño; HUD en amarillo si > x1
- 8 tests nuevos (`test_gameplay_v16.py`, `test_enemy_flash.py`) — total 274 tests

---

## [1.5.0] — Nuevos power-ups: spread, plasma, laser

### 1.5.2
- `Player.shoot()`: spread (5 balas abanico ±30°) y plasma (Shot6 lento, 5 daño) con precedencia sobre gun_upgrade
- `GameplayScene`: grupo `lasers`, activación con Space, daño continuo LASER_DAMAGE_PER_S×dt
- 7 tests nuevos (`test_laser.py` + `test_player.py`)

### 1.5.1
- Constantes `SPREAD_ANGLES`, `SPREAD_DAMAGE`, `PLASMA_SPEED_MULT`, `PLASMA_DAMAGE`, `PLASMA_TINT`, `LASER_*` en settings
- Entidad `Laser`: rayo de área 8px, dura 3s, daña 10 HP/s a enemigos en columna, se autodestruye
- `PowerUp` acepta 3 nuevos tipos: `spread`, `plasma`, `laser` (sprites placeholder)

---

## [1.4.0] — Power-ups con identidad visual

### 1.4.2
- `MenuScene`: hover con ratón resalta opción, click izquierdo activa

### 1.4.1
- `Bullet` guarda `self.tint` para introspección en tests
- `GUN_UPGRADE_DIVERGE_DEG = 8.0` en settings
- `Player.shoot()`: balas laterales con `angle_deg` proporcional por nivel (±4°, ±8°, ±16°)
- `shield` activo: todas las balas con tint blanco-azul
- `rapid_fire` activo: tint azul neón + damage reducido al 50%
- Ambos powerups activos: sin crash, shield sobreescribe tint, damage de rapidfire se mantiene
- 6 tests nuevos en `test_player.py`

---

## [1.3.0] — Disparos avanzados: base técnica

### 1.3.4
- Flechas del teclado (↑↓←→) como alternativa a WASD en gameplay
- ENTER como alternativa a SPACE en game over (fallback headless)

### 1.3.3
- `GameplayScene`: colisiones de bala usan `bullet.damage` en lugar de constante global `BULLET_DAMAGE`

### 1.3.2
- `Player.shoot()` pasa `damage` y `tint` a cada `Bullet` según powerups activos
- `rapid_fire`: damage = max(1, DEFAULT * 0.5), tint azul neón
- `shield`: tint blanco-azul (sin cambio de damage)

### 1.3.1
- `Bullet` acepta `angle_deg` (movimiento diagonal), `damage` por instancia, `tint` RGBA, `speed_mult`
- Helper `_apply_tint()` aplica tint a todos los frames via `BLEND_RGBA_MULT`
- Kill check extendido a bordes izquierdo/derecho de pantalla
- 6 tests nuevos en `test_bullet.py` (total 253 tests)

---

## [1.2.0] — Menus, pausa, records locales

### Added
- `MenuScene` con 3 opciones navegables (JUGAR / RECORDS / SALIR), flechas o W/S, ENTER/SPACE
- `GameOverScene` con entrada de iniciales (hasta 3 chars) si entra en top 10
- `ScoresScene` — tabla top 10 con posición, iniciales y score
- `src/systems/scores.py` — `load()`, `save()`, `qualifies()`, JSON en `~/.starfall/scores.json`
- Pausa en gameplay con `P` o `ESC`; segundo `ESC` vuelve al menú
- Stack de escenas en `Game`: `push_scene()` / `pop_scene()` / `replace_scene()`
- `src/settings/scores.py` — `MAX_SCORE_ENTRIES`, `SCORES_FILE`
- 12 tests nuevos (`test_scores.py`, `test_menu.py`) — total 247 tests

### Changed
- `Game` ahora gestiona `_stack: list` en lugar de `self.scene` único
- `GameplayScene.__init__` acepta `game=None` para integración con stack
- Estado inicial de gameplay cambia de `"start"` a `"playing"` (el menú ocupa ese rol)
- Al morir el player, transiciona a `GameOverScene` en lugar de quedarse en gameplay

### chore
- Archivos de audio SFX y música de gameplay agregados al repo (`assets/audio/`)

---

## [1.1.0] — AudioSystem

### Added
- `AudioSystem` singleton (`src/systems/audio.py`): `init()`, `play_sfx()`, `play_music()`, `toggle_mute()`
- Música de gameplay en loop (`assets/audio/music/gameplay.ogg`)
- SFX para disparo, impacto, explosión, powerup, daño al player, game over, boss hit
- Tecla `M` silencia/restaura todo el audio en tiempo real
- Carga lazy: no-op tolerante si el archivo no existe
- `src/settings/audio.py` con rutas y volúmenes configurables
- 12 tests en `test_audio.py` — total 235 tests

---

## [1.0.0] — SpaceRage sprites + ScrollingBG

### Added
- Player SpaceRage sprites with 5-pose directional banking animation (l2/l1/m/r1/r2)
- Player shadow sprites rendered beneath ship with configurable offset
- Scrolling parallax background (BG.png, two-tile infinite scroll)
- Rocket power-up wired into POWERUP_KINDS

### Changed
- Asset consolidation: all sprites reorganized into clean folders (bg/, player/, enemies/, enemy_fx/, explosions/, powerups/, Shots/)
- Shield overlay repositioned above player ship (no longer overlapping hull)
- CLAUDE.md rewritten to reflect current project state

### Fixed
- BG gap bug: tile height forced to max(SCREEN_H, aspect_fit_height) to prevent ghost sprite trails
- Shield overlay covering player view
- test_assets.py path after asset consolidation
- Stripped invalid iCCP chunks from SpaceRage PNG pack (187 files)

---

## [0.9.0] — Animated bullets + 6 enemy types

### Added
- Animated player bullets with launch / travel / impact phases per shot level
- Animated enemy projectiles using SpaceRage FX sprites (plasma, proton, vulcan)
- 6th enemy type: Interceptor (tracks player, 1500 pts)
- Escalating difficulty curve across all 6 enemy types
- Settings modularized into src/settings/ package (screen, player, enemies, boss, waves, powerups, sprites, explosions)

### Fixed
- ImpactEffect added to explosions group so update() is called each frame

---

## [0.8.0] — Rockets + 6-level shot progression

### Added
- Dual angled rockets (Rocket power-up fires 2 rockets at ±ROCKET_ANGLE_DEG)
- 6 distinct shot levels with unique sprites (Shot1–Shot4) and display sizes 50×50 – 90×90
- Area-damage explosion on rocket impact (ROCKET_RADIUS)

---

## [0.7.2] — Asset fix

### Fixed
- Stripped incorrect iCCP sRGB chunks from enemy ship PNG files (libpng warnings at runtime)

---

## [0.7.1] — Death explosions

### Added
- Entity death explosions: all 9 explosion sequences assigned per entity type
- Boss uses oversized explosion (160×160); all others 80×80
- ImpactEffect for bullet hit feedback

---

## [0.7.0] — Boss wave trigger

### Changed
- Boss triggers every BOSS_WAVE_INTERVAL waves instead of on a fixed timer

---

## [0.6.0] — Boss enemy

### Added
- Boss entity with 2-phase combat: spread shots (phase 1) → rapid fire (phase 2)
- Ping-pong horizontal movement pattern
- Boss health bar in HUD
- Boss sprite rotation every BOSS_SPRITES_FIXED_COUNT waves (4 variants)
- SpawnSystem integration: boss spawns every 10 waves; wave resets after boss kill

### Fixed
- Boss y-position clamped to BOSS_Y_TARGET on entry completion
- EnemyBullet killed on horizontal screen exit
- Spread shot angle via angle_deg parameter on EnemyBullet

---

## [0.5.0] — Kamikaze + Power-ups

### Added
- Kamikaze enemy: homing movement targeting player position (500 pts)
- PowerUp entity with 5 kinds: rapid_fire, shield, gun_upgrade, rocket, extra_life
- Player active_powerups tracking; shield absorbs 1 hit
- apply_powerup() integrates all 5 types
- Lazy asset cache (src/assets.py)
- 20% power-up drop chance on enemy kill

---

## [0.4.0] — Enemy bullets + Wave spawning

### Added
- EnemyBullet entity with angle_deg spread support
- Fighter.shoot() and Scout speed_bonus
- SpawnSystem with wave progression: 30s or 10 kills advances wave
- Wave-based enemy speed and spawn interval scaling
- Enemy bullets integrated into GameplayScene collision detection

---

## [0.3.0] — Score, lives, HUD

### Added
- Score tracking (per-enemy points)
- Player lives (3 default, max 5) with invincibility frames on hit
- Game states: start → playing → game_over (overlay + restart)
- HUD: score, wave, lives hearts

---

## [0.2.0] — Enemies + collisions

### Added
- Scout enemy (straight movement, 1 HP, 100 pts)
- Fighter enemy (zigzag movement, 3 HP, 250 pts)
- Enemy base class
- Bullet-enemy collision (spritecollide)
- Enemy spawning integrated into GameplayScene
- Resolution changed to 540×960 (9:16 portrait)

---

## [0.1.0] — Window, player, movement, shooting

### Added
- Pygame window (540×960, 60 FPS)
- Player entity with WASD + arrow key movement and screen boundary clamping
- Bullet entity with upward travel and off-screen culling
- Space bar shooting with configurable cooldown
- Game loop: process_input → update → render
- Scene architecture (GameplayScene)
- Settings module with all constants
