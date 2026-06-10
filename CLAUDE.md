# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

**Starfall** — Shoot 'em up vertical 2D, inspirado en 1942/Raiden/Tyrian.
- Python 3.13+, Pygame Community Edition
- Resolución: 540×960, modo ventana, 60 FPS objetivo
- Plataformas: Windows 11 y Linux

## Comandos

```bash
# Ejecutar el juego
python main.py

# Instalar dependencia principal
pip install pygame-ce

# Ejecutar tests
python -m pytest tests/
```

## Arquitectura

`main.py` solo instancia y lanza el juego. Toda la lógica vive en `src/`.

**Flujo central:**
```
main.py → Game (src/game.py) → Scene activa → Entities + Systems
```

**Capas:**

| Capa | Ubicación | Responsabilidad |
|------|-----------|-----------------|
| Escenas | `src/scenes/` | Estados del juego (start, gameplay, game_over) |
| Entidades | `src/entities/` | Sprites con lógica propia |
| Sistemas | `src/systems/` | Lógica transversal (spawning) |
| Config | `src/settings/` | Paquete modular; importar desde `src.settings` |
| Assets | `src/assets.py` | Carga y caché centralizada; rutas relativas a `assets/` |

**Game loop en `src/scenes/gameplay.py`:**
```python
process_input() → update() → render()
```
`update()` llama explícitamente a cada grupo: `bullets`, `rockets`, `explosions`, `enemies`, `enemy_bullets`, `powerups`. El grupo `all_sprites` se usa **solo para render**, nunca se le llama `update()`.

## Convenciones

- Clases: `PascalCase` (`Player`, `Enemy`, `Boss`)
- Funciones/variables: `snake_case` (`spawn_enemy()`, `player_health`)
- Sin números mágicos — todo en `src/settings/`
- Sin lógica de juego en `main.py`
- Sin variables globales innecesarias
- Colisiones vía `pygame.sprite.spritecollide()` / `pygame.sprite.groupcollide()`

## Entidades

| Entidad | Archivo | Descripción |
|---------|---------|-------------|
| `Player` | `player.py` | 5 poses banked (SpaceRage), lerp `_bank` hacia `vel_x` |
| `ScrollingBG` | `scrolling_bg.py` | Fondo scroll vertical con 2 tiles |
| `Scout` | `scout.py` | Movimiento recto, 1 HP, 100 pts |
| `Fighter` | `fighter.py` | Zigzag, 3 HP, 250 pts, dispara plasma |
| `Kamikaze` | `kamikaze.py` | Persigue player, 2 HP, 500 pts |
| `Gunner` | `gunner.py` | Disparo 3 vías vulcan |
| `Striker` | `striker.py` | Burst 2 balas apuntadas proton |
| `Interceptor` | `interceptor.py` | Disparo único apuntado plasma |
| `Boss` | `boss.py` | 2 fases, barra HP, sprites rotativos, 5000 pts |
| `Bullet` | `bullet.py` | 3 fases: launch → travel → impacto; `impact_frames` para `ImpactEffect` |
| `EnemyBullet` | `enemy_bullet.py` | Animación en loop, velocidad por ángulo |
| `Rocket` | `rocket.py` | Misil con radio de daño |
| `ImpactEffect` | `impact_effect.py` | One-shot al morir bala; **debe agregarse a `explosions` group** para que reciba `update(dt)` |
| `Explosion` | `explosion.py` | One-shot death animation |
| `PowerUp` | `powerup.py` | Tipos: `rapid_fire`, `shield`, `gun_upgrade`, `extra_life`, `rocket` |

## Settings (`src/settings/`)

| Módulo | Contenido |
|--------|-----------|
| `screen.py` | `SCREEN_W=540`, `SCREEN_H=960`, `FPS=60`, `BG_SCROLL_SPEED` |
| `player.py` | `PLAYER_W/H=64`, `PLAYER_SPEED`, `PLAYER_BANK_LERP`, `BULLET_*`, `HUD_*` |
| `enemies.py` | Stats de los 6 tipos de enemigos + `ENEMY_BULLET_*` |
| `waves.py` | Parámetros de oleadas |
| `powerups.py` | `POWERUP_*` |
| `sprites.py` | Todas las rutas de assets; listas de frames para disparos y proyectiles enemigos |
| `boss.py` | `BOSS_*`, `ROCKET_*`, `BOSS_SPRITES` |
| `explosions.py` | Listas de frames de explosiones; aliases `EXPL_*` por tipo de enemigo |

## Assets (`assets/`)

| Carpeta | Contenido |
|---------|-----------|
| `bg/` | `bg.png` — fondo scrolling |
| `player/` | 5 poses cuerpo (`l2/l1/m/r1/r2.png`) + 5 shadows + `shield_overlay.png` |
| `powerups/` | `rapid_fire`, `shield`, `gun_upgrade`, `extra_life`, `rocket` |
| `enemies/` | `scout/fighter/kamikaze/gunner/striker/interceptor.png` + `boss1-4.png` + `missile.png` |
| `enemy_fx/` | `plasma_1-2.png`, `proton_01-03.png`, `vulcan_1-3.png` |
| `explosions/` | `fx1-3/` (genéricas) + `ship1-6/` (muerte por tipo) |
| `Shots/` | `Shot1-6/` — frames launch/travel/impact por nivel de disparo |

## Disparo del player

6 niveles, controlados por `player.shot_level`. Cada bala tiene 3 fases animadas:
- **launch**: frames one-shot al crear
- **travel**: sprite estático mientras viaja
- **impact**: spawn de `ImpactEffect` al colisionar (agregar a `explosions` group)

## Controles

| Tecla | Acción |
|-------|--------|
| WASD | Mover |
| Espacio | Disparar |
| Espacio (en start/game over) | Reiniciar |
| ESC | Salir |

## Roadmap

| Versión | Estado | Contenido |
|---------|--------|-----------|
| v0.1–v0.9 | ✅ taggeados | Ventana, player, enemigos, colisiones, puntuación, power-ups, jefe, sprites SpaceRage, animaciones |
| v1.0 | 🔨 en desarrollo | Menús, sonido, guardado de récords |

## Git Workflow

- `main` — releases estables, solo merges desde `develop`, taggeado (`v0.x`)
- `develop` — integración, base para ramas de trabajo

**Ramas de trabajo:** `v{major}.{minor}/descripcion-corta`

**Flujo:**
1. `git checkout develop && git checkout -b v1.0/tema`
2. Trabajar y commitear en la rama
3. `git checkout develop && git merge v1.0/tema`
4. Al cerrar versión: `git checkout main && git merge develop && git tag v1.0`
