# Boss Enemy (v0.6) — Design Spec

## Goal

Agregar un Boss semi-infinito que aparece cada 2 minutos, rota entre 4 sprites de Enemy, tiene 2 fases de combate y una barra de vida en el HUD.

## Architecture

Approach A: Boss como subclase de `Enemy`, `SpawnSystem` gestiona el timer y la rotación de sprites.

```
SpawnSystem.get_boss_spawn(now)
  → Boss(sprite_path)
  → GameplayScene: añade a enemies + self.boss
  → Boss.shoot(now) → list[EnemyBullet]
  → boss muere → SpawnSystem.notify_boss_killed(now) → programa próximo boss
```

Boss vive en el grupo `enemies` — las colisiones existentes (bullet-enemy, player-enemy) lo manejan sin cambios.

## Files

| Archivo | Acción |
|---|---|
| `src/entities/boss.py` | Nuevo |
| `src/entities/enemy_bullet.py` | Modifica — agrega `angle_deg=0` |
| `src/systems/spawning.py` | Modifica — timer, rotación sprites |
| `src/scenes/gameplay.py` | Modifica — `self.boss`, barra de vida, shoot del boss |
| `src/settings.py` | Modifica — constantes BOSS_* y BOSS_SPRITES |
| `tests/test_boss.py` | Nuevo |
| `tests/test_enemy_bullet.py` | Modifica — tests de disparo diagonal |
| `tests/test_spawning.py` | Modifica — tests de boss timer |

## Settings

```python
BOSS_W = 96
BOSS_H = 80
BOSS_HP = 30
BOSS_POINTS = 5000
BOSS_SPEED = 150            # px/s horizontal (ping-pong y entrada)
BOSS_Y_TARGET = 120         # Y donde termina entrada y empieza ping-pong
BOSS_SHOOT_INTERVAL_P1 = 1500   # ms entre disparos, fase 1
BOSS_SHOOT_INTERVAL_P2 = 1000   # ms entre disparos, fase 2
BOSS_SPREAD_ANGLE = 20          # grados, abanico fase 2
BOSS_HEALTH_BAR_H = 12
BOSS_TRIGGER_MS = 120_000       # ms hasta primera aparición (2 min)
BOSS_SPRITES = [
    "enemy/Enemy_1_A.png",
    "enemy/Enemy_2_A.png",
    "enemy/Enemy_3_A.png",
    "enemy/Enemy_4_A.png",
]
BOSS_SPRITES_FIXED_COUNT = 3    # primeras 3 apariciones en orden; luego aleatorio
```

## Boss Class — `src/entities/boss.py`

```python
class Boss(Enemy):
    def __init__(self, sprite_path: str):
        super().__init__(SCREEN_W // 2, BOSS_W, BOSS_H, (0, 0, 0), BOSS_HP, BOSS_POINTS)
        raw = assets.get(sprite_path)
        self.image = pygame.transform.scale(raw, (BOSS_W, BOSS_H))
        self.rect = self.image.get_rect(centerx=SCREEN_W // 2, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.phase: int = 1
        self.dir: int = 1           # ping-pong: +1 derecha, -1 izquierda
        self.last_shot: int = -BOSS_SHOOT_INTERVAL_P1
        self._entry_done: bool = False
```

### Movimiento

1. **Entrada:** Boss baja verticalmente desde `y = -BOSS_H` hasta `y = BOSS_Y_TARGET` a `BOSS_SPEED` px/s.
2. **Ping-pong:** Una vez `_entry_done`, se mueve horizontalmente. Invierte `dir` al tocar los bordes (`rect.left <= 0` o `rect.right >= SCREEN_W`).
3. Boss **no llama** `super().update(dt)` — no se elimina al salir de pantalla.

### Fases

```python
self.phase = 1 if self.hp > BOSS_HP // 2 else 2
```

- **Fase 1** (`hp > 15`): un disparo recto cada `BOSS_SHOOT_INTERVAL_P1` ms.
- **Fase 2** (`hp <= 15`): abanico de 3 balas (ángulos `-BOSS_SPREAD_ANGLE`, `0`, `+BOSS_SPREAD_ANGLE`) cada `BOSS_SHOOT_INTERVAL_P2` ms.

### shoot()

```python
def shoot(self, now: int) -> list[EnemyBullet]:
    interval = BOSS_SHOOT_INTERVAL_P1 if self.phase == 1 else BOSS_SHOOT_INTERVAL_P2
    if now - self.last_shot < interval:
        return []
    self.last_shot = now
    cx, bottom = self.rect.centerx, self.rect.bottom
    if self.phase == 1:
        return [EnemyBullet(cx, bottom)]
    return [
        EnemyBullet(cx, bottom, -BOSS_SPREAD_ANGLE),
        EnemyBullet(cx, bottom, 0),
        EnemyBullet(cx, bottom, +BOSS_SPREAD_ANGLE),
    ]
```

## EnemyBullet — Disparo Diagonal

Agrega parámetro `angle_deg=0` (grados desde vertical, positivo = derecha):

```python
import math

def __init__(self, x, y, angle_deg=0):
    rad = math.radians(angle_deg)
    self._vx = math.sin(rad) * ENEMY_BULLET_SPEED
    self._vy = math.cos(rad) * ENEMY_BULLET_SPEED
    self.x = float(self.rect.x)   # sub-pixel X
    # self.y ya existe

def update(self, dt):
    self.x += self._vx * dt
    self.y += self._vy * dt
    self.rect.x = int(self.x)
    self.rect.y = int(self.y)
```

Retrocompatible — `angle_deg=0` produce movimiento recto idéntico al actual.

## SpawnSystem — Boss Timer

### Nuevos atributos

```python
self._boss_spawn_at: int = BOSS_TRIGGER_MS
self._boss_index: int = 0
self.boss_alive: bool = False
```

### Nuevos métodos

```python
def get_boss_spawn(self, now: int) -> Boss | None:
    if self.boss_alive or now < self._boss_spawn_at:
        return None
    sprite = self._next_boss_sprite()
    self.boss_alive = True
    self._boss_index += 1
    return Boss(sprite)

def notify_boss_killed(self, now: int) -> None:
    self.boss_alive = False
    self._boss_spawn_at = now + BOSS_TRIGGER_MS

def _next_boss_sprite(self) -> str:
    if self._boss_index < BOSS_SPRITES_FIXED_COUNT:
        return BOSS_SPRITES[self._boss_index]
    return random.choice(BOSS_SPRITES)
```

### Pausa de spawning normal

En `SpawnSystem.update()`, si `self.boss_alive`, retorna `[]` sin generar enemigos normales.

## GameplayScene — Integración

### `__init__` y `_reset`

```python
self.boss: Boss | None = None
```

### `update()`

```python
# Spawn boss
b = self.spawn_system.get_boss_spawn(now)
if b:
    self.boss = b
    self.enemies.add(b)
    self.all_sprites.add(b)

# Boss dispara
if self.boss and self.boss.alive():
    for eb in self.boss.shoot(now):
        self.enemy_bullets.add(eb)
        self.all_sprites.add(eb)

# Boss muerto
if self.boss and not self.boss.alive():
    self.spawn_system.notify_boss_killed(now)
    self.boss = None
```

### `render()` — Barra de vida

Dibujada debajo del texto SCORE (no encima), solo cuando boss está vivo:

```python
if self.boss and self.boss.alive():
    bar_w = SCREEN_W - 2 * HUD_MARGIN
    filled = int(bar_w * self.boss.hp / BOSS_HP)
    y = HUD_MARGIN + HUD_FONT_SIZE + 6
    pygame.draw.rect(screen, (80, 0, 0),    (HUD_MARGIN, y, bar_w, BOSS_HEALTH_BAR_H))
    pygame.draw.rect(screen, (220, 30, 30), (HUD_MARGIN, y, filled, BOSS_HEALTH_BAR_H))
    pygame.draw.rect(screen, (255, 255, 255),(HUD_MARGIN, y, bar_w, BOSS_HEALTH_BAR_H), 1)
```

## Testing

### `tests/test_boss.py`

- Boss spawna centrado en top (rect.centerx == SCREEN_W // 2, rect.bottom == 0)
- Boss baja durante entrada hasta BOSS_Y_TARGET
- Boss hace ping-pong: invierte dir al tocar borde derecho / izquierdo
- Fase 1 shoot retorna 1 bala cuando cooldown cumplido
- Fase 2 shoot retorna 3 balas
- Transición fase 1→2 cuando hp <= BOSS_HP // 2
- `shoot()` respeta cooldown (retorna [] si muy pronto)

### `tests/test_enemy_bullet.py`

- `EnemyBullet(x, y)` sin ángulo: vx == 0, vy == ENEMY_BULLET_SPEED (retrocompat)
- `EnemyBullet(x, y, 20)`: vx > 0, vy > 0, speed total == ENEMY_BULLET_SPEED
- `EnemyBullet(x, y, -20)`: vx < 0
- Bullet diagonal se mueve en ambos ejes tras `update(1.0)`

### `tests/test_spawning.py`

- `get_boss_spawn(now < BOSS_TRIGGER_MS)` retorna None
- `get_boss_spawn(now >= BOSS_TRIGGER_MS)` retorna Boss
- Segunda llamada inmediata retorna None (boss_alive=True)
- `notify_boss_killed(now)` → `get_boss_spawn(now + BOSS_TRIGGER_MS - 1)` = None
- `notify_boss_killed(now)` → `get_boss_spawn(now + BOSS_TRIGGER_MS)` = Boss
- Primeras 3 apariciones usan BOSS_SPRITES[0..2] en orden
- Aparición 4+ es aleatoria (mock random.choice)
- `update()` retorna [] mientras boss_alive=True

## Semi-infinito

No hay victoria permanente. Ciclo indefinido:
1. Oleadas normales por 2 min
2. Boss aparece, oleadas pausan
3. Boss muere → `notify_boss_killed` → +2 min hasta próximo boss
4. Volver a 1

El sprite del boss rota: Enemy_1 → Enemy_2 → Enemy_3 → aleatorio entre los 4.
