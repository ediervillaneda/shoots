# Starfall

Vertical 2D shoot-'em-up built with Python 3.13+ and pygame-ce.

Inspired by Raiden, 1942, Tyrian, and Aero Fighters.

## Quick start

```bash
pip install pygame-ce
python main.py
```

## Features

- 6 enemy types (Scout, Fighter, Kamikaze, Gunner, Striker, Interceptor)
- Boss fights every 10 waves with 2-phase attack patterns
- 6 weapon levels with launch/travel/impact animations
- 5 power-ups (rapid fire, shield, gun upgrade, rocket, extra life)
- 5-directional player banking sprite
- Scrolling parallax background
- Wave-based progression with scaling difficulty

## Controls

| Key | Action |
|-----|--------|
| `W/A/S/D` or arrows | Move |
| `Space` | Shoot |
| `ESC` | Quit |

## Project structure

```
main.py                # Entry point
src/
  game.py              # Game loop, init, quit
  assets.py            # Lazy-loading image cache
  settings/            # All constants (split by domain)
  entities/            # Player, enemies, bullets, explosions, powerups
  scenes/              # GameplayScene (process_input / update / render)
  systems/             # SpawnSystem (wave progression, enemy spawning)
tests/                 # 229 tests, pytest
assets/                # ~300 sprites across 6 source directories
```

## Documentation

| File | Contents |
|------|----------|
| `docs/technical.md` | Install, play, architecture, modding |
| `assets/README.md` | Asset inventory, entity-to-sprite mapping |
| `assets/Shots/SPRITES.md` | Shot sprite animation guide |

## Version

v1.0 — 229 tests passing.
