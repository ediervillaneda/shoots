# AGENTS.md -- Starfall

**Idioma:** Espanol (Espanol), o ingles cuando el contexto lo requiera.

## Proyecto

Starfall: shoot 'em up vertical 2D (Python 3.13+, pygame-ce).
Resolucion: 540x960 ventana, objetivo 60 FPS.
Version actual: **v1.1** (235 tests).

## Comandos

```bash
python main.py                               # Ejecutar el juego
pip install pygame-ce                        # Instalar dependencia
python build_release.py                      # Generar .exe (Windows)
pytest -v                                    # Todos los tests
pytest -v tests/test_player.py               # Archivo especifico
pytest -v tests/test_player.py::test_nombre  # Test especifico
pytest -v --cov=src                          # Con cobertura
pyinstaller Starfall.spec                    # Build manual (alternativa)
```

No hay linter/formatter configurado. No hay `pyproject.toml`.

## Arquitectura

```
main.py -> Game (src/game.py) -> GameplayScene -> Entities + Systems
```

- `main.py`: entrypoint, sin logica de juego.
- `src/game.py`: game loop -- `clock.tick(60)`, `process_input` -> `update(dt)` -> `render(screen)`. Llama `audio.init()` antes de crear la escena.
- `src/scenes/gameplay.py`: estados `start`/`playing`/`game_over`. Grupo `all_sprites` **solo para render** (nunca `.update()`). Cada grupo de entidades se actualiza individualmente (`bullets`, `rockets`, `enemies`, `enemy_bullets`, `powerups`, `explosions`).
- `src/settings/`: paquete de 9 modulos. Importar via `from src.settings import ...` o `from src.settings.audio import ...`.
- `src/assets.py`: cache lazy de imagenes -- `assets.get("path.png")` devuelve `pygame.Surface` cacheado. Rutas relativas a `assets/`. Maneja `sys._MEIPASS` de PyInstaller.
- `src/systems/audio.py`: modulo singleton de audio. Ver seccion AudioSystem.
- **Build**: `python build_release.py` (verifica requisitos, corre tests, llama PyInstaller). CI en `.github/workflows/release.yml`.

## Entidades (17 archivos en `src/entities/`)

Todos los sprites en movimiento almacenan `self.x`/`self.y` como `float`,
aplican movimiento via deltas `dt`, luego `self.rect.x = int(self.x)` cada frame.

| Entidad | Archivo | Notas |
|---------|---------|-------|
| Player | `player.py` | 5 poses banked (l2/l1/m/r1/r2), lerp `_bank` hacia `vel_x`. 6 niveles de disparo, contador de rockets. |
| Bullet | `bullet.py` | 3 fases: launch frames -> travel estatico -> impact frames (spawnea `ImpactEffect`). |
| Rocket | `rocket.py` | Dano directo `ROCKET_DAMAGE` + dano en area `ROCKET_AREA_DAMAGE` dentro de `ROCKET_RADIUS`. |
| Scout | `scout.py` | Recto hacia abajo, 1 HP, 100 pts. |
| Fighter | `fighter.py` | Zigzag, 2 HP, 250 pts, dispara plasma. |
| Kamikaze | `kamikaze.py` | Persigue player, 2 HP, 500 pts. |
| Gunner | `gunner.py` | Spread 3 balas vulcan, oleada 3+, 5 HP, 600 pts. |
| Striker | `striker.py` | Entrada diagonal -> rafagas proton apuntadas, oleada 6+, 8 HP, 1000 pts. |
| Interceptor | `interceptor.py` | Entrada rapida -> patrulla + disparo continuo, oleada 10+, 15 HP, 1500 pts. |
| Boss | `boss.py` | 2 fases (hp>50%: disparo unico; <=50%: spread 3 balas). **No llama `super().update(dt)`** (entrada fuera de pantalla). Ping-pong horizontal tras descender a `BOSS_Y_TARGET`. |
| EnemyBullet | `enemy_bullet.py` | Con angulo -- `EnemyBullet(x, y, angle_deg=0, ...)`. Muere al salir por cualquier borde. |
| PowerUp | `powerup.py` | 5 tipos: `rapid_fire`, `shield`, `gun_upgrade`, `rocket`, `extra_life`. |
| Explosion | `explosion.py` | Animacion por frames, `Explosion(cx, cy, paths, size)`. One-shot. |
| ImpactEffect | `impact_effect.py` | One-shot al impactar bala. **Debe agregarse al grupo `explosions`** para recibir `update(dt)`. |
| ScrollingBG | `scrolling_bg.py` | No es Sprite. Scroll vertical con 2 tiles. Metodo `draw(screen)`. |

**Base de enemigos** (`enemy.py`): subclases llaman `super().__init__(x, w, h, color, hp, points)` y `super().update(dt)` al final. `take_damage(amount)` decrementa hp, llama `self.kill()` en <=0.

**Speed bonus** (escala por oleada):
```python
self.y += (BASE_SPEED + getattr(self, "speed_bonus", 0.0)) * dt
```

**Colisiones**: `pygame.sprite.groupcollide()` / `spritecollide()`. Balas del jugador `dokill=True`, enemigos `dokill=False` (manual `take_damage`). Rocket: `spritecollide(rocket, enemies, False)` + verificacion manual de radio.

## Settings (`src/settings/`)

| Modulo | Contenido |
|--------|-----------|
| `screen.py` | `SCREEN_W=540`, `SCREEN_H=960`, `FPS=60`, `BG_SCROLL_SPEED` |
| `player.py` | `PLAYER_W/H=64`, `PLAYER_SPEED`, `PLAYER_BANK_LERP`, `BULLET_*`, `HUD_*` |
| `enemies.py` | Stats de los 6 tipos de enemigos + `ENEMY_BULLET_*` |
| `waves.py` | Umbrales de oleadas, oleadas de desbloqueo, tasas de spawn |
| `powerups.py` | `POWERUP_DROP_CHANCE`, tamano, velocidad |
| `sprites.py` | Todas las rutas de assets; listas de frames; `SPRITE_HEART` |
| `boss.py` | `BOSS_*`, `ROCKET_*`, `BOSS_SPRITES` |
| `explosions.py` | Listas de frames de explosiones; aliases `EXPL_*` por tipo de entidad |
| `audio.py` | `MUSIC_VOLUME=0.5`, `SFX_VOLUME=0.7`, rutas `SFX_*` y `MUSIC_*` |

## AudioSystem (`src/systems/audio.py`)

Modulo singleton. Carga lazy con cache. Tolerante a archivos faltantes (no crashea si no existen).

```python
import src.systems.audio as audio

audio.init()              # Inicializar mixer (una vez, en Game.__init__)
audio.play_sfx(path)      # Reproducir SFX; no-op si archivo falta o esta muteado
audio.play_music(path)    # Musica en loop -1; no-op si archivo falta
audio.stop_music()        # Detener musica
audio.toggle_mute()       # Silenciar/restaurar todo (tecla M)
audio.is_muted()          # bool
audio.clear_cache()       # Vaciar cache (usar en tests)
```

Archivos de audio: `assets/audio/sfx/*.wav` y `assets/audio/music/*.ogg`.
Directorios presentes en repo pero vacios -- el juego arranca sin archivos.

**Puntos de evento en GameplayScene:**
- Disparo bala -> `SFX_SHOOT`
- Impacto bala en enemigo -> `SFX_IMPACT`
- Muerte de enemigo/boss -> `SFX_EXPLOSION`
- Boss recibe dano (sobrevive) -> `SFX_BOSS_HIT`
- Player recoge power-up -> `SFX_POWERUP`
- Player pierde vida -> `SFX_PLAYER_HIT`
- Game over (una vez) -> `SFX_GAME_OVER`
- Musica de fondo en loop -> `MUSIC_GAMEPLAY`

## Estilo de codigo

**Imports** (en orden): stdlib -> pygame -> local. Separados con lineas en blanco.
```python
import math
import random

import pygame

import src.assets as assets
from src.entities.player import Player
from src.settings import SCREEN_W, FPS
```

- Clases: `PascalCase`. Funciones/variables: `snake_case`. Constantes: `UPPER_CASE`. Privados: `_leading_underscore`.
- Sin docstrings en codigo trivial. Sin espacios al final. 2 lineas en blanco antes de clases, 1 entre metodos.
- Sin numeros magicos -- todo en `src/settings/`. Sin try/except para control de flujo.
- Anotaciones de tipo minimales (`kind: str`, `dt: float`, `-> None`), no forzadas.

## Convenciones de tests

- **pytest** unicamente (235 tests, 18 archivos en `tests/`). Sin `unittest.TestCase`.
- **conftest.py**: fixture `pygame_init` (scope=session, drivers SDL dummy) + `clear_asset_cache` (scope=function).
- **Nombres**: `tests/test_<modulo>.py` espeja `src/entities/<modulo>.py`. Funciones: `test_<snake_case>`.
- **Patron**: preparar entidad -> ejecutar accion -> `assert` directo. Usar `pytest.approx()` para floats.
- **Mocking**: `unittest.mock.patch` para controlar `random` (`side_effect`), `pygame.time.get_ticks()` en tests de Boss.
- **Aislamiento**: entidades frescas por test. `pygame.sprite.Group(entity)` al testear `kill()`.

## Roadmap

| Version | Estado | Scope |
|---------|--------|-------|
| v0.1 | DONE | Ventana 540x960, Player, movimiento WASD, disparo, game loop |
| v0.2 | DONE | Scout, Fighter, colisiones, SpawnSystem basico |
| v0.3 | DONE | Score, 3 vidas, HUD, estados start/playing/game_over |
| v0.4 | DONE | EnemyBullet, Fighter.shoot(), oleadas con escalado de velocidad e intervalo |
| v0.5 | DONE | Kamikaze, PowerUp (5 tipos), apply_powerup(), cache lazy de assets |
| v0.6 | DONE | Boss (2 fases), barra HP, ping-pong horizontal, 4 sprites rotativos por oleadas |
| v0.7 | DONE | Boss cada BOSS_WAVE_INTERVAL oleadas; explosiones de muerte por tipo de entidad |
| v0.8 | DONE | Rocket (2 angulados, dano en area), 6 niveles de disparo con sprites por nivel |
| v0.9 | DONE | Bullets animados 3 fases, EnemyBullet animado, Interceptor, dificultad escalada |
| v1.0 | DONE | Sprites SpaceRage (5 poses banked + shadows), ScrollingBG, shield_overlay |
| v1.1 | DONE | AudioSystem singleton, SFX en 7 eventos, musica en loop, mute tecla M -- 235 tests |
| v1.2 | TODO | Stack de escenas; MenuScene; GameplayScene con pausa; GameOverScene con entrada de iniciales; ScoresScene; scores.py persistencia JSON local |
| v1.3 | TODO | Bullet con angle_deg y damage por instancia; tinting de balas segun power-up activo |
| v1.4 | TODO | gun_upgrade dispara con divergencia lateral; shield activo muestra halo blanco-azul en balas; rapid_fire tint azul + damage reducido |
| v1.5 | TODO | Nuevos power-ups: spread (5 balas +/-30 grados), plasma (Shot6 lento damage 5), laser (entidad rayo de area activo 3s) |
| v1.6 | TODO | Screen shake al morir/boss; combo multiplier x1-x8 en HUD; flash blanco 80ms en enemigos al recibir dano |
| v1.7 | TODO | Flanker (entrada lateral, disparo hacia el centro); Raider (sube desde abajo); formaciones cunia de Scouts desde oleada 5 |
| v1.8 | TODO | Gunner dispara burst de 3; 8 balas 360 grados al morir; HomingBullet para Interceptor; lead shot para Striker |
| v1.9 | TODO | Modos Endless / Survival / Daily (seed diaria) con scores separados; nuevo enemigo Orbiter con orbita circular (oleada 12+) |
| v2.0 | TODO | Boss fase 3 (patron frenesi + espiral 16 balas); slow motion 0.3x al matar boss; disparo auto toggle; balance general; release final |

## Git workflow

- `main` -- releases estables, merges desde `develop`, taggeado (`v1.x`).
- `develop` -- base de integracion para ramas de trabajo.
- Ramas: `v{major}.{minor}/descripcion-corta` (ej: `v1.2/menu-principal`).
- Flujo: `develop` -> rama -> trabajo/commits -> merge a `develop` -> `main` + tag al cerrar version.
- Estilo de commits: `tipo(scope): mensaje` -- `feat(v1.2):`, `fix(v1.1):`, `test(v1.2):`, `refactor:`, `docs:`, `release(v1.1):`.

## No hacer

- Poner logica de juego en `main.py`.
- Usar numeros magicos fuera de `src/settings/`.
- Variables globales innecesarias.
- Importar desde `src.systems` dentro de archivos de entidades (entidades importan solo settings + assets).
- Mutar `rect.x`/`rect.y` sin mantener coordenadas float.
- Llamar `super().update(dt)` en `Boss.update()`.
- Olvidar agregar nuevos grupos de entidades a `GameplayScene._reset()` y `__init__`.
- Crear configuraciones `pyproject.toml` sin discutirlo primero.
