# CLAUDE.md

Instrucciones para Claude cuando trabaja en este repositorio.
Para referencia tecnica completa ver AGENTS.md.

## Proyecto

**Starfall** -- Shoot 'em up vertical 2D, inspirado en 1942/Raiden/Tyrian.
- Python 3.13+, Pygame Community Edition
- Resolucion: 540x960, modo ventana, 60 FPS objetivo
- Plataformas: Windows 11 y Linux

## Comandos

```bash
# Ejecutar el juego
python main.py

# Instalar dependencia principal
pip install pygame-ce

# Ejecutar tests
python -m pytest tests/

# Generar ejecutable (.exe en Windows)
python build_release.py
```

## Arquitectura

`main.py` solo instancia y lanza el juego. Toda la logica vive en `src/`.

**Flujo central:**
```
main.py -> Game (src/game.py) -> Scene activa -> Entities + Systems
```

**Capas:**

| Capa | Ubicacion | Responsabilidad |
|------|-----------|-----------------|
| Escenas | `src/scenes/` | Estados del juego (start, gameplay, game_over) |
| Entidades | `src/entities/` | Sprites con logica propia |
| Sistemas | `src/systems/` | Logica transversal (spawning, audio) |
| Config | `src/settings/` | Paquete modular; importar desde `src.settings` |
| Assets | `src/assets.py` | Carga y cache centralizada; rutas relativas a `assets/` |

**Game loop en `src/scenes/gameplay.py`:**
```python
process_input() -> update() -> render()
```
`update()` llama explicitamente a cada grupo: `bullets`, `rockets`, `explosions`,
`enemies`, `enemy_bullets`, `powerups`. El grupo `all_sprites` se usa **solo para
render**, nunca se le llama `update()`.

## Convenciones

- Clases: `PascalCase` (`Player`, `Enemy`, `Boss`)
- Funciones/variables: `snake_case` (`spawn_enemy()`, `player_health`)
- Sin numeros magicos -- todo en `src/settings/`
- Sin logica de juego en `main.py`
- Sin variables globales innecesarias
- Colisiones via `pygame.sprite.spritecollide()` / `pygame.sprite.groupcollide()`
- Coordenadas de movimiento en `float` (`self.x`, `self.y`); `rect` se actualiza como `int` cada frame

## Entidades

| Entidad | Archivo | Descripcion |
|---------|---------|-------------|
| `Player` | `player.py` | 5 poses banked (SpaceRage), lerp `_bank` hacia `vel_x` |
| `ScrollingBG` | `scrolling_bg.py` | Fondo scroll vertical con 2 tiles |
| `Scout` | `scout.py` | Movimiento recto, 1 HP, 100 pts |
| `Fighter` | `fighter.py` | Zigzag, 2 HP, 250 pts, dispara plasma |
| `Kamikaze` | `kamikaze.py` | Persigue player, 2 HP, 500 pts |
| `Gunner` | `gunner.py` | Disparo 3 vias vulcan, 5 HP, 600 pts |
| `Striker` | `striker.py` | Burst proton apuntado, 8 HP, 1000 pts |
| `Interceptor` | `interceptor.py` | Patrulla + disparo rapido, 15 HP, 1500 pts |
| `Boss` | `boss.py` | 2 fases, barra HP, sprites rotativos, 5000 pts |
| `Bullet` | `bullet.py` | 3 fases: launch -> travel -> impacto; `impact_frames` para `ImpactEffect` |
| `EnemyBullet` | `enemy_bullet.py` | Animacion en loop, velocidad por angulo |
| `Rocket` | `rocket.py` | Misil con radio de dano |
| `ImpactEffect` | `impact_effect.py` | One-shot al morir bala; **debe agregarse a `explosions` group** |
| `Explosion` | `explosion.py` | One-shot death animation |
| `PowerUp` | `powerup.py` | Tipos: `rapid_fire`, `shield`, `gun_upgrade`, `extra_life`, `rocket` |

## Settings (`src/settings/`)

| Modulo | Contenido |
|--------|-----------|
| `screen.py` | `SCREEN_W=540`, `SCREEN_H=960`, `FPS=60`, `BG_SCROLL_SPEED` |
| `player.py` | `PLAYER_W/H=64`, `PLAYER_SPEED`, `PLAYER_BANK_LERP`, `BULLET_*`, `HUD_*` |
| `enemies.py` | Stats de los 6 tipos de enemigos + `ENEMY_BULLET_*` |
| `waves.py` | Parametros de oleadas |
| `powerups.py` | `POWERUP_*` |
| `sprites.py` | Todas las rutas de assets; listas de frames para disparos y proyectiles |
| `boss.py` | `BOSS_*`, `ROCKET_*`, `BOSS_SPRITES` |
| `explosions.py` | Listas de frames de explosiones; aliases `EXPL_*` por tipo de enemigo |
| `audio.py` | `MUSIC_VOLUME`, `SFX_VOLUME`, rutas SFX y musica |

## Assets (`assets/`)

| Carpeta | Contenido |
|---------|-----------|
| `bg/` | `bg.png` -- fondo scrolling |
| `player/` | 5 poses cuerpo (`l2/l1/m/r1/r2.png`) + 5 shadows + `shield_overlay.png` |
| `powerups/` | `rapid_fire`, `shield`, `gun_upgrade`, `extra_life`, `rocket` |
| `enemies/` | `scout/fighter/kamikaze/gunner/striker/interceptor.png` + `boss1-4.png` + `missile.png` |
| `enemy_fx/` | `plasma_1-2.png`, `proton_01-03.png`, `vulcan_1-3.png` |
| `explosions/` | `fx1-3/` (genericas) + `ship1-6/` (muerte por tipo) |
| `Shots/` | `Shot1-6/` -- frames launch/travel/impact por nivel de disparo |
| `audio/sfx/` | Efectos de sonido WAV (vacios; agregar para activar) |
| `audio/music/` | Musica de fondo OGG (vacia; agregar para activar) |

## AudioSystem (`src/systems/audio.py`)

Modulo singleton. Carga lazy, tolerante a archivos faltantes.

| Funcion | Descripcion |
|---------|-------------|
| `audio.init()` | Inicializar mixer (llamar en `Game.__init__`) |
| `audio.play_sfx(path)` | Reproducir SFX; no-op si archivo no existe o esta muteado |
| `audio.play_music(path)` | Musica en loop; no-op si archivo no existe |
| `audio.toggle_mute()` | Tecla M -- silencia/restaura todo |

## Controles

| Tecla | Accion |
|-------|--------|
| WASD | Mover |
| Espacio | Disparar |
| M | Mute/unmute audio |
| Espacio (en start/game over) | Reiniciar |
| ESC | Salir |

## Roadmap

| Version | Estado | Contenido |
|---------|--------|-----------|
| v0.1-v0.9 | DONE | Ventana, player, enemigos, colisiones, puntuacion, power-ups, jefe, sprites, animaciones |
| v1.1 | DONE | AudioSystem: SFX + musica de fondo + mute (235 tests) |
| v1.2 | TODO | Menu principal |
| v1.3 | TODO | Guardado de records |
| v1.4+ | TODO | Balance, pulido, extras |

## Git Workflow

- `main` -- releases estables, solo merges desde `develop`, taggeado (`v1.x`)
- `develop` -- integracion, base para ramas de trabajo

**Ramas de trabajo:** `v{major}.{minor}/descripcion-corta`

**Flujo:**
1. `git checkout develop && git checkout -b v1.2/tema`
2. Trabajar y commitear en la rama
3. `git checkout develop && git merge v1.2/tema`
4. Al cerrar version: `git checkout main && git merge develop && git tag v1.2`
