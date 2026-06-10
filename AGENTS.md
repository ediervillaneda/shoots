# AGENTS.md — Starfall

## Project overview

Starfall: vertical 2D shoot-'em-up (Python 3.13+, pygame-ce).  
Resolution: 540×960 windowed, target 60 FPS.  
Platforms: Windows 11, Linux.  
Current version: **v0.7.2** (188 tests).

## Commands

```bash
# Run game
python main.py

# Install dependency
pip install pygame-ce

# Run all tests
pytest -v

# Run single test file
pytest -v tests/test_player.py

# Run single test function
pytest -v tests/test_player.py::test_player_initial_position

# Run with coverage
pytest -v --cov=src

# Run with output capture disabled
pytest -v -s tests/test_file.py
```

No linter/formatter configured. No `pyproject.toml`. `pytest` uses default discovery (`tests/` folder, `test_*.py`).

## Architecture

```
main.py → Game (src/game.py) → Scene → Entities + Systems
```

- `main.py`: instantiate & launch `Game`. No game logic.
- `src/scenes/gameplay.py`: game states (start/playing/game_over). Three-method API: `process_input(events)`, `update(dt)`, `render(screen)`.
- `src/entities/`: `pygame.sprite.Sprite` subclasses (player, bullet, rocket, enemy, scout, fighter, kamikaze, boss, enemy_bullet, powerup, explosion).
- `src/systems/spawning.py`: `SpawnSystem` — wave progression, enemy creation, boss trigger.
- `src/settings.py`: all constants and tunable parameters (188 lines).
- `src/assets.py`: lazy image cache — `assets.get("path.png")` returns cached `pygame.Surface`.

## Code style

**Imports** (in order): standard library → third-party (pygame) → local. Group with blank lines.

```python
import math
import random

import pygame

import src.assets as assets
from src.entities.player import Player
from src.settings import SCREEN_W, FPS
```

**Naming:**
- Classes: `PascalCase` (`Player`, `Boss`, `GameplayScene`, `SpawnSystem`)
- Functions/variables: `snake_case` (`take_damage`, `calc_velocity`, `active_powerups`, `speed_bonus`, `shoot_rocket`)
- Constants: `UPPER_CASE` (`PLAYER_SPEED`, `BOSS_HP`, `WAVE_KAMIKAZE_CAP`, `EXPL_SCOUT`)
- Private methods: `_leading_underscore` (`_reset`, `_spawn_interval`, `_maybe_drop_powerup`, `_draw_overlay`, `_spawn_death_explosion`, `_handle_player_damage`, `_explode`)

**Formatting:**
- No docstrings or comments on trivial code. Docstrings only on complex methods.
- 2 blank lines before class definitions, 1 between methods. No trailing whitespace.
- Compare with `is`/`is not` for singletons (`None`), `==` for values.
- No magic numbers — put every tunable in `settings.py`.

**Types:** minimal type annotations. Accepted for clarity (`kind: str`, `-> None`, `-> list[Bullet]`, `-> list[EnemyBullet]`, `dt: float`, `now: int`), not enforced.

**Error handling:** no try/except. Game-critical assumptions (assets exist, pygame inits) expected to hold or crash. Tests use `pytest.raises` only if needed.

## Entities

**Enemy base** (`enemy.py`): subclasses call `super().__init__(x, w, h, color, hp, points)` then `super().update(dt)` at end. `take_damage(amount)` decrements hp, calls `self.kill()` at ≤0. **Boss skips `super().update(dt)`** (it manages its own lifecycle outside screen bounds).

**Position tracking:** all moving sprites store `self.x`/`self.y` as `float`, apply movement via `dt` deltas, then `self.rect.x = int(self.x)`, `self.rect.y = int(self.y)` each frame. `EnemyBullet` uses `self._vx`/`self._vy` for angled movement.

**Speed bonus** (wave scaling):
```python
self.y += (BASE_SPEED + getattr(self, "speed_bonus", 0.0)) * dt
```

**Boss:** 2-phase fight. Phase 1 (hp > 50%): single shot. Phase 2 (hp ≤ 50%): 3-shot spread (`BOSS_SPREAD_ANGLE`). Ping-pong horizontal movement after descending to `BOSS_Y_TARGET`. Spawned by `SpawnSystem.get_boss_spawn()` every `BOSS_WAVE_INTERVAL` waves, rotating through `BOSS_SPRITES`. Health bar rendered in HUD.

**Rocket:** player area-damage weapon. `ROCKET_DAMAGE` direct + `ROCKET_AREA_DAMAGE` within `ROCKET_RADIUS` (px). Power-up key: `"rocket"`. Triggers `_explode()` on hit, which damages all enemies in radius.

**Explosion:** frame-animated sprite. `Explosion(cx, cy, paths, size)` — plays through `paths` list, one frame per `EXPLOSION_FRAME_MS`, then `self.kill()`. Entity-specific frame sets in settings (`EXPL_SCOUT`, `EXPL_FIGHTER`, `EXPL_KAMIKAZE`, `EXPL_BOSS`, `EXPL_PLAYER`).

**EnemyBullet:** angled constructor — `EnemyBullet(x, y, angle_deg=0)`. Uses `math.sin`/`cos` for `_vx`/`_vy`. Killed on any edge exit (top, left, right). Boss phase 2 spawns 3 bullets at `{-20°, 0°, +20°}`.

**Power-ups:** 5 kinds — `"rapid_fire"`, `"shield"`, `"gun_upgrade"`, `"rocket"`, `"extra_life"`. Stored in `Player.active_powerups: set[str]`. `shot_level: int` (1–3) controls bullet count via `"gun_upgrade"`. Rocket uses separate `shoot_rocket()` with its own cooldown.

**Shot sprites (per level):**
- Level 1: `Shots/Shot1/shot1_4.png` (50×50)
- Level 2: `Shots/Shot2/shot2_4.png` (75×75)
- Level 3: `Shots/Shot4/shot4_asset.png` (80×80)

**Collisions:** always via `pygame.sprite.spritecollide()` / `pygame.sprite.groupcollide()`. Player bullets `True` (killed on hit), enemies `False` (manual `take_damage`). Rocket collision: `spritecollide(rocket, enemies, False)` + manual kill + `_explode()`.

## Test conventions

- **pytest** only — no `unittest.TestCase`, no test classes.
- **conftest.py**: `pygame_init` (session-scoped, dummy SDL drivers) + `clear_asset_cache` (function-scoped).
- **File naming:** `tests/test_<module>.py` mirrors `src/entities/<module>.py`.
- **Test naming:** `test_<descriptive_snake_case>`.
- **Arrange/Act/Assert:** setup entity → run action → plain `assert`. Use `pytest.approx()` for floats.
- **Mocking:** `unittest.mock.patch` for random control (`side_effect` to force probabilities). `unittest.mock.patch` for `pygame.time.get_ticks()` in boss timing tests.
- **Isolation:** each test creates fresh entities. `pygame.sprite.Group(entity)` when testing `kill()`.
- **Sprite-dependent entities** (Boss, Scout, Fighter, Kamikaze, Bullet, Rocket, Explosion, PowerUp) require `conftest.py` fixtures to load from disk.

## Git workflow

- `main` — releases estables, solo merges desde `develop`, taggeado (v0.1, v0.2...)
- `develop` — integración, base para crear ramas de trabajo

**Ramas de trabajo:** `v0.x/descripcion-corta` (ej: `v0.1/player-movement`)

**Flujo:**
1. `git checkout develop && git checkout -b v0.x/tema`
2. Trabajar y commitear en la rama
3. `git checkout develop && git merge v0.x/tema`
4. Al cerrar versión: `git checkout main && git merge develop && git tag v0.x`

Commit style: `type(scope): message` — `feat(v0.7):`, `fix(v0.7):`, `test(v0.7):`, `refactor:`, `docs:`, `release(v0.7):`.

## Directories

```
src/
  game.py            # Game class (init, run loop)
  settings.py        # All constants (188 lines)
  assets.py          # Lazy image cache
  entities/          # Player, Bullet, Rocket, Enemy, Scout, Fighter, Kamikaze,
                     # Boss, EnemyBullet, PowerUp, Explosion
  scenes/            # GameplayScene (process_input/update/render)
  systems/           # SpawnSystem (wave progression, enemy creation, boss trigger)
tests/               # Mirror src/ structure, test_*.py (13 files)
assets/              # images (ship/, enemy/, Shots/, Explosions/)
```

## Do not

- Put game logic in `main.py`. Use magic numbers (define in `settings.py`). Add unnecessary globals.
- Import from `src.systems` inside entity files (entities import settings + assets only).
- Use `try/except` for flow control.
- Mutate `rect.x`/`rect.y` without tracking float coords (causes drift at low dt).
- Call `super().update(dt)` in `Boss.update()` (kills boss for being off-screen during entry).
- Forget to add new entity groups to `GameplayScene._reset()` and `__init__`.
- Create `pyproject.toml`-level tool configs without discussion.
