# AGENT.md

## Proyecto

Nombre: Starfall (nombre provisional)

Tipo: Shoot 'em up (Shmup) 2D

Plataforma objetivo:
- Windows 11
- Linux (Arch Linux incluido)

Tecnología principal:
- Python 3.13+
- Pygame Community Edition

Resolución inicial:
- 480x640 píxeles
- Modo ventana

Control:
- Teclado

---

# Objetivo

Desarrollar un shoot 'em up vertical clásico inspirado en:

- 1942
- Raiden
- Tyrian
- Aero Fighters

El jugador controla una nave espacial que debe sobrevivir a oleadas de enemigos, acumular puntos y derrotar jefes.

---

# Principios de Desarrollo

1. Código simple antes que código complejo.
2. Evitar optimizaciones prematuras.
3. Mantener módulos pequeños y desacoplados.
4. Priorizar jugabilidad sobre efectos visuales.
5. Cada funcionalidad debe ser fácilmente extensible.

---

# Estructura del Proyecto

```text
project/
│
├── main.py
│
├── src/
│   ├── game.py
│   ├── settings.py
│   ├── assets.py
│   │
│   ├── entities/
│   │   ├── player.py
│   │   ├── bullet.py
│   │   ├── enemy.py
│   │   ├── boss.py
│   │   └── powerup.py
│   │
│   ├── systems/
│   │   ├── collision.py
│   │   ├── spawning.py
│   │   ├── scoring.py
│   │   └── audio.py
│   │
│   └── scenes/
│       ├── menu.py
│       ├── gameplay.py
│       ├── pause.py
│       └── gameover.py
│
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
│
└── saves/
```

---

# Mecánicas Iniciales

## Jugador

Características:

- Movimiento en 8 direcciones
- Disparo automático o manual
- 3 vidas iniciales
- Invulnerabilidad temporal tras recibir daño

Controles:

| Tecla | Acción |
|---------|---------|
| W | Arriba |
| S | Abajo |
| A | Izquierda |
| D | Derecha |
| Espacio | Disparar |
| P | Pausa |
| ESC | Salir |

---

## Balas

Características:

- Movimiento vertical
- Eliminación automática fuera de pantalla
- Daño configurable

Parámetros:

```python
damage = 1
speed = 12
```

---

## Enemigos

Tipos iniciales:

### Scout

- Movimiento recto
- Vida: 1

### Fighter

- Movimiento en zigzag
- Vida: 3

### Kamikaze

- Persigue al jugador
- Vida: 2

---

## Jefe

Características:

- Aparición cada cierto puntaje
- Múltiples patrones de disparo
- Barra de vida

---

## Sistema de Puntuación

| Evento | Puntos |
|----------|----------|
| Scout | 100 |
| Fighter | 250 |
| Kamikaze | 500 |
| Boss | 5000 |

---

## Power-Ups

Tipos:

### Rapid Fire

Incrementa velocidad de disparo.

### Shield

Absorbe un impacto.

### Double Shot

Dispara dos proyectiles.

### Triple Shot

Dispara tres proyectiles.

---

# Sistema de Oleadas

Cada oleada debe:

- Incrementar dificultad
- Incrementar velocidad enemiga
- Incrementar frecuencia de aparición

Fórmula inicial:

```python
enemy_speed = base_speed + wave * 0.2
```

---

# Sistema de Colisiones

Detectar:

- Bala jugador vs enemigo
- Bala enemigo vs jugador
- Nave vs enemigo
- Nave vs power-up

Utilizar:

```python
pygame.sprite.spritecollide()
```

---

# Estados del Juego

## Menú

Opciones:

- Nueva partida
- Configuración
- Salir

---

## Gameplay

Estado principal.

---

## Pausa

Congela:

- Movimiento
- Enemigos
- Disparos

---

## Game Over

Mostrar:

- Puntaje
- Récord
- Reintentar

---

# Sonido

Eventos mínimos:

- Disparo
- Explosión
- Power-up
- Boss warning
- Game over

Formato recomendado:

```text
wav
ogg
```

---

# Rendimiento

Objetivo:

```python
FPS = 60
```

Nunca bloquear el game loop.

---

# Game Loop Esperado

```python
while running:

    process_input()

    update()

    detect_collisions()

    render()

    clock.tick(60)
```

---

# Convenciones de Código

## Nombres

Clases:

```python
Player
Enemy
Boss
```

Funciones:

```python
spawn_enemy()
update_score()
create_bullet()
```

Variables:

```python
player_health
enemy_speed
current_wave
```

---

# No Hacer

Evitar:

- Variables globales innecesarias
- Lógica de juego en main.py
- Código duplicado
- Números mágicos
- Dependencias innecesarias

---

# Roadmap

## Versión 0.1

- Ventana
- Nave
- Movimiento
- Disparo

## Versión 0.2

- Enemigos
- Colisiones

## Versión 0.3

- Puntuación
- Vidas

## Versión 0.4

- Power-ups

## Versión 0.5

- Jefe final

## Versión 1.0

- Menús
- Sonido
- Guardado de récords
- Balance general

---

# Criterio de Éxito

Se considera exitosa la versión 1.0 cuando:

- El juego es completamente jugable con teclado.
- Mantiene 60 FPS constantes.
- Tiene al menos 3 tipos de enemigos.
- Tiene al menos 1 jefe.
- Guarda récords localmente.
- No presenta errores críticos durante 30 minutos continuos de juego.
