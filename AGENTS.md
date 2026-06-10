# AGENTS.md — Starfall

## Project

Starfall: vertical 2D shoot-'em-up (Python 3.13+, pygame-ce).  
Resolution: 540×960 windowed, target 60 FPS.  
Version: **v1.0** (229 tests).

## Commands

```bash
python main.py                          # Run game
pip install pygame-ce                   # Install dependency
pytest -v                               # All tests
pytest -v tests/test_player.py          # Single file
pytest -v tests/test_player.py::test_<name>  # Single test
pytest -v --cov=src                     # Coverage
pyinstaller Starfall.spec               # Build standalone binary
```

No linter/formatter configured. No `pyproject.toml`.

## Architecture

```
main.py → Game (src/game.py) → GameplayScene → Entities + Systems
```

- `main.py`: entrypoint, no game logic.
- `src/game.py`: game loop — `clock.tick(60)`, `process_input` → `update(dt)` → `render(screen)`.
- `src/scenes/gameplay.py`: states `start`/`playing`/`game_over`. `all_sprites` group for **render only** (never `.update()`). Each entity group is updated individually (`bullets`, `rockets`, `enemies`, `enemy_bullets`, `powerups`, `explosions`).
- `src/settings/`: package, 8 domain modules (`screen`, `player`, `enemies`, `waves`, `powerups`, `sprites`, `boss`, `explosions`). Import via `from src.settings import ...`.
- `src/assets.py`: lazy image cache — `assets.get("path.png")` returns cached `pygame.Surface`. Paths relative to `assets/`. Handles PyInstaller `sys._MEIPASS`.
- **Build**: `pyinstaller Starfall.spec` (CI release workflow at `.github/workflows/release.yml`).

## Entities (17 files in `src/entities/`)

All moving sprites store `self.x`/`self.y` as `float`, apply movement via `dt` deltas, then `self.rect.x = int(self.x)` each frame.

| Entity | File | Notes |
|--------|------|-------|
| Player | `player.py` | 5 banking poses (l2/l1/m/r1/r2), lerp `_bank` toward `vel_x`. 6 shot levels, rocket count. |
| Bullet | `bullet.py` | 3-phase anim: launch frames → travel static → impact frames (spawns `ImpactEffect`). |
| Rocket | `rocket.py` | Area-damage weapon. `ROCKET_DAMAGE` direct + `ROCKET_AREA_DAMAGE` within `ROCKET_RADIUS`. |
| Scout | `scout.py` | Straight down, 1 HP, 100 pts. |
| Fighter | `fighter.py` | Zigzag, 2 HP, 250 pts, shoots plasma. |
| Kamikaze | `kamikaze.py` | Chases player, 2 HP, 500 pts. |
| Gunner | `gunner.py` | 3-bullet spread vulcan, wave 3+, 5 HP. |
| Striker | `striker.py` | Diagonal entry → aimed proton bursts, wave 6+, 8 HP. |
| Interceptor | `interceptor.py` | Fast entry → patrol + rapid fire, wave 10+, 15 HP. |
| Boss | `boss.py` | 2 phases (hp>50%: single shot; ≤50%: 3-shot spread). **Skips `super().update(dt)`** (off-screen entry). Ping-pong horizontal after descending to `BOSS_Y_TARGET`. |
| EnemyBullet | `enemy_bullet.py` | Angled — `EnemyBullet(x, y, angle_deg=0, ...)`. Killed on any edge exit. |
| PowerUp | `powerup.py` | 5 kinds: `rapid_fire`, `shield`, `gun_upgrade`, `rocket`, `extra_life`. |
| Explosion | `explosion.py` | Frame-animated, `Explosion(cx, cy, paths, size)`. One-shot. |
| ImpactEffect | `impact_effect.py` | One-shot bullet impact anim. **Must be added to `explosions` group** to get `update(dt)`. |
| ScrollingBG | `scrolling_bg.py` | Not a Sprite. 2-tile vertical scroll. `draw(screen)` method. |

**Enemy base** (`enemy.py`): subclasses call `super().__init__(x, w, h, color, hp, points)` then `super().update(dt)` at end. `take_damage(amount)` decrements hp, calls `self.kill()` at ≤0.

**Speed bonus** (wave scaling):
```python
self.y += (BASE_SPEED + getattr(self, "speed_bonus", 0.0)) * dt
```

**Collisions**: `pygame.sprite.groupcollide()` / `spritecollide()`. Player bullets `dokill=True`, enemies `dokill=False` (manual `take_damage`). Rocket: `spritecollide(rocket, enemies, False)` + manual radius check.

## Code style

**Imports** (in order): standard library → pygame → local. Group with blank lines.
```python
import math
import random

import pygame

import src.assets as assets
from src.entities.player import Player
from src.settings import SCREEN_W, FPS
```

- Classes: `PascalCase`. Functions/vars: `snake_case`. Constants: `UPPER_CASE`. Private: `_leading_underscore`.
- No docstrings on trivial code. No trailing whitespace. 2 blank lines before classes, 1 between methods.
- No magic numbers — everything in `src/settings/`. No try/except for flow control.
- Minimal type annotations (`kind: str`, `dt: float`, `-> None`, `-> list[Bullet]`), not enforced.

## Test conventions

- **pytest** only (229 tests, 17 files in `tests/`). No `unittest.TestCase`.
- **conftest.py**: `pygame_init` (session-scoped, dummy SDL drivers) + `clear_asset_cache` (function-scoped).
- **Naming**: `tests/test_<module>.py` mirrors `src/entities/<module>.py`. Functions: `test_<snake_case>`.
- **Pattern**: arrange entity → run action → plain `assert`. Use `pytest.approx()` for floats.
- **Mocking**: `unittest.mock.patch` for random control (`side_effect`), `pygame.time.get_ticks()` in boss timing tests.
- **Isolation**: fresh entities per test. `pygame.sprite.Group(entity)` when testing `kill()`.
- **Sprite entities** (Boss, Scout, Fighter, Kamikaze, Bullet, Rocket, Explosion, PowerUp, etc.) load from disk via conftest fixtures.

## Git workflow

- `main` — stable releases, merged from `develop`, tagged (`v0.x`, `v1.0`).
- `develop` — integration base for feature branches.
- Branches: `v{major}.{minor}/descricao-curta` (e.g. `v0.1/player-movement`).
- Flow: `develop` → branch → work/commit → merge to `develop` → `main` + tag on release.
- Commit style: `type(scope): message` — `feat(v0.7):`, `fix(v0.7):`, `test(v0.7):`, `refactor:`, `docs:`, `release(v0.7):`.

## Do not

- Put game logic in `main.py`. Use magic numbers. Add unnecessary globals.
- Import from `src.systems` inside entity files (entities import settings + assets only).
- Mutate `rect.x`/`rect.y` without tracking float coords.
- Call `super().update(dt)` in `Boss.update()`.
- Forget to add new entity groups to `GameplayScene._reset()` and `__init__`.
- Create `pyproject.toml`-level tool configs without discussion.
