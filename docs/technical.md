# Technical Documentation

## Install

### Requirements

- Python 3.13+
- [pygame-ce](https://github.com/pygame-community/pygame-ce) 2.5+

### Setup

```bash
# Install dependency
pip install pygame-ce

# Run the game
python main.py
```

### Running tests

```bash
# All tests
pytest -v

# Single file
pytest -v tests/test_player.py

# With coverage
pytest -v --cov=src
```

229 tests — no additional dependencies required.

## How to play

### Objective

Survive waves of enemies, defeat the boss every 10 waves, and score as many points as possible. You have 3 lives (max 5 with power-ups).

### Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move up |
| `S` / `↓` | Move down |
| `A` / `←` | Move left |
| `D` / `→` | Move right |
| `Space` (hold) | Shoot / Start game / Restart |
| `ESC` | Quit |

### Scoring

| Enemy | Points |
|-------|--------|
| Scout | 100 |
| Fighter | 250 |
| Kamikaze | 500 |
| Gunner | 600 |
| Striker | 1000 |
| Interceptor | 1500 |
| Boss | 5000 |

### Power-ups

Drop chance: 20% on enemy kill.

| Power-up | Effect |
|----------|--------|
| Rapid fire | Increases fire rate (cooldown ×0.4) |
| Shield | Absorbs 1 hit |
| Gun upgrade | Increases shot level (1–6) |
| Rocket | Fires area-damage rockets (max 2 active) |
| Extra life | +1 life (up to 5 max) |

### Shot levels

| Level | Bullets | Sprite | Display size |
|-------|---------|--------|-------------|
| 1 | 1 | Shot1 | 50×50 |
| 2 | 2 | Shot2 | 75×75 |
| 3 | 3 | Shot2 | 75×75 |
| 4 | 3 | Shot4 | 80×80 |
| 5 | 4 | Shot4 | 85×85 |
| 6 | 4 | Shot4 | 90×90 |

## Architecture

### Game loop (`src/game.py`)

```python
while running:
    dt = clock.tick(60) / 1000.0
    scene.process_input(events)
    scene.update(dt)
    scene.render(screen)
    pygame.display.flip()
```

### Scene API

All gameplay lives in `GameplayScene` with a 3-method interface:

- `process_input(events)` — handles keyboard, state transitions
- `update(dt)` — moves entities, spawns enemies, detects collisions
- `render(screen)` — draws everything

### Entity lifecycle

1. **Spawning**: `SpawnSystem.update(now)` returns a list of new enemies based on wave timers and kill thresholds
2. **Update**: Each entity updates position via `x`/`y` floats → `rect.x`/`rect.y` ints
3. **Collision**: `pygame.sprite.groupcollide()` / `spritecollide()` — bullets kill on hit, enemies use `take_damage()`
4. **Death**: Entity dies → death explosion animation → optional power-up drop → score increment

### Wave system

Waves advance when either:
- 30 seconds have passed since last wave
- 10 enemies have been killed since last wave

Each wave increases enemy speed by `WAVE_SPEED_FACTOR` (0.2) and reduces spawn interval by 150 ms (capped at 600 ms).

New enemy types unlock at specific waves:
- Wave 3: Gunner
- Wave 6: Striker
- Wave 10: Interceptor + Boss

### Settings system

All constants live in `src/settings/` split by domain:

| File | Contents |
|------|----------|
| `screen.py` | SCREEN_W, SCREEN_H, FPS, TITLE |
| `player.py` | Player speed, size, bullet cooldown, HUD |
| `enemies.py` | Scout, Fighter, Kamikaze, Gunner, Striker, Interceptor stats |
| `boss.py` | Boss HP, speed, shoot intervals, rocket stats |
| `waves.py` | Wave thresholds, unlock waves, spawn rates |
| `powerups.py` | Drop chance, size, speed |
| `sprites.py` | All asset path constants |
| `explosions.py` | Explosion frame paths, render sizes |

## Modding

### Adding a new enemy type

1. Add stats in `src/settings/enemies.py`
2. Create entity class in `src/entities/` (subclass `Enemy`)
3. Add sprite path in `src/settings/sprites.py`
4. Add explosion mapping in `src/settings/explosions.py`
5. Register in `src/scenes/gameplay.py` (import, group, `_spawn_death_explosion`)
6. Add wave unlock config in `src/settings/waves.py`
7. Add spawning logic in `src/systems/spawning.py`
8. Add tests in `tests/`

### Asset conventions

- All sprites loaded via `src.assets.get(path)` — lazy caches `pygame.Surface`
- Moving sprites store `self.x`/`self.y` as float, convert to `rect.x`/`rect.y` as int each frame
- Animations use frame lists + elapsed time, not `pygame.time.set_timer()`
- Every tunable number belongs in `src/settings/` — no magic numbers

### Code style

- Imports: standard library → third-party (pygame) → local, grouped with blank lines
- Classes: `PascalCase`, functions/variables: `snake_case`, constants: `UPPER_CASE`
- Private methods: `_leading_underscore`
- No docstrings on trivial code
- No try/except for flow control
- Compare singletons with `is`/`is not`, values with `==`

## Asset pipeline

```
assets/              # All source assets
├── bg/               # Background tile (bg.png)
├── player/           # Player body (5 poses), shadows (5 poses), shield overlay
├── enemies/          # 6 enemy sprites + 4 boss sprites + missile
├── enemy_fx/         # Enemy projectile FX (plasma, proton, vulcan)
├── explosions/       # 9 explosion frame sequences (fx1-3, ship1-6)
├── powerups/         # 5 power-up icons
└── Shots/            # 6 shot types × 3 phases (launch/travel/impact)

src/assets.py         # Lazy image cache — assets.get("path.png")
↓
Entity constructor    # pygame.transform.scale() to render size
```

## Known technical notes

- Boss skips `super().update(dt)` from `Enemy` (it manages its own lifecycle outside screen bounds)
- Explosion frame timing: 55 ms per frame (~550–660 ms total for 10–12 frames)
- Player has 5 directional banking sprites (`l2`, `l1`, `m`, `r1`, `r2`) with lerp interpolation
- Rocket collision uses `spritecollide(rocket, enemies, False)` + manual radius check
- Shadow sprite rendered below player with configurable offset
