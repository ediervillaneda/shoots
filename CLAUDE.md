# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

**Starfall** — Shoot 'em up vertical 2D, inspirado en 1942/Raiden/Tyrian.
- Python 3.13+, Pygame Community Edition
- Resolución: 480×640, modo ventana, 60 FPS objetivo
- Plataformas: Windows 11 y Linux

## Comandos

```bash
# Ejecutar el juego
python main.py

# Instalar dependencia principal
pip install pygame-ce

# Ejecutar con salida de debug (si se implementa)
python main.py --debug
```

No hay framework de tests todavía. Al agregar tests, usar `pytest`.

## Arquitectura

`main.py` solo instancia y lanza el juego. Toda la lógica vive en `src/`.

**Flujo central:**
```
main.py → Game (src/game.py) → Scene activa → Entities + Systems
```

**Capas:**

| Capa | Ubicación | Responsabilidad |
|------|-----------|-----------------|
| Escenas | `src/scenes/` | Estados del juego (menu, gameplay, pause, gameover) |
| Entidades | `src/entities/` | Sprites con lógica propia (player, enemy, boss, bullet, powerup) |
| Sistemas | `src/systems/` | Lógica transversal sin estado propio (collision, spawning, scoring, audio) |
| Config | `src/settings.py` | Todas las constantes y parámetros ajustables |
| Assets | `src/assets.py` | Carga centralizada de imágenes, sonidos y fuentes |

**Game loop esperado en `src/scenes/gameplay.py`:**
```python
process_input() → update() → detect_collisions() → render()
```

## Convenciones

- Clases: `PascalCase` (`Player`, `Enemy`, `Boss`)
- Funciones/variables: `snake_case` (`spawn_enemy()`, `player_health`)
- Sin números mágicos — todo en `settings.py`
- Sin lógica de juego en `main.py`
- Sin variables globales innecesarias
- Colisiones vía `pygame.sprite.spritecollide()`

## Entidades y parámetros clave

**Enemigos:**
- `Scout`: movimiento recto, vida 1, 100 pts
- `Fighter`: zigzag, vida 3, 250 pts
- `Kamikaze`: persigue jugador, vida 2, 500 pts
- `Boss`: múltiples patrones, barra de vida, 5000 pts

**Escalado de dificultad:**
```python
enemy_speed = base_speed + wave * 0.2
```

**Power-ups:** `RapidFire`, `Shield`, `DoubleShot`, `TripleShot`

**Controles:** WASD mover, Espacio disparar, P pausar, ESC salir.

## Roadmap actual

- v0.1: Ventana, nave, movimiento, disparo
- v0.2: Enemigos, colisiones
- v0.3: Puntuación, vidas
- v0.4: Power-ups
- v0.5: Jefe
- v1.0: Menús, sonido, guardado de récords
