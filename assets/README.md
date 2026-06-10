# Starfall — Asset Inventory

7 directories, ~300 sprites. Detailed shot animation guide in `Shots/SPRITES.md`.

## Directory overview

| Directory | Contents | Used in code |
|-----------|----------|--------------|
| `bg/` | Background tile | ✅ ScrollingBG |
| `player/` | Player body (5 poses), shadows (5 poses), shield overlay | ✅ Player |
| `enemies/` | 6 enemy sprites + 4 boss sprites + missile | ✅ All enemies, Boss, Rocket |
| `enemy_fx/` | Enemy projectile FX (plasma, proton, vulcan) | ✅ Scout/Fighter/Gunner/Striker/Interceptor |
| `explosions/` | 9 frame sequences across 9 subdirs | ✅ All entity death explosions |
| `powerups/` | 5 power-up icons | ✅ PowerUp entity |
| `Shots/` | 6 shot types × 3 phases (launch/travel/impact) | ✅ Level 1–6 bullets |

## In-use sprite map

### Player

| Asset | Path | Render size |
|-------|------|-------------|
| Body — 5 poses (l2/l1/m/r1/r2) | `player/{pose}.png` | 64×64 |
| Shadow — 5 poses | `player/shadow_{pose}.png` | 64×64 |
| Shield overlay | `player/shield_overlay.png` | PLAYER_W+20 × PLAYER_H+20 |

### Enemies

| Entity | Sprite | Render size |
|--------|--------|-------------|
| Scout | `enemies/scout.png` | 40×40 |
| Fighter | `enemies/fighter.png` | 44×44 |
| Kamikaze | `enemies/kamikaze.png` | 48×48 |
| Gunner | `enemies/gunner.png` | 52×52 |
| Striker | `enemies/striker.png` | 56×56 |
| Interceptor | `enemies/interceptor.png` | 60×60 |
| Boss (rotates per wave) | `enemies/boss{1..4}.png` | 96×80 |

### Projectiles

| Projectile | Path | Render size |
|------------|------|-------------|
| Player bullets (levels 1–6) | `Shots/Shot{1..6}/` (launch + travel + impact) | 50×50 – 90×90 |
| Plasma | `enemy_fx/plasma_{1,2}.png` | 12×42 |
| Proton | `enemy_fx/proton_0{1..3}.png` | 22×22 |
| Vulcan | `enemy_fx/vulcan_{1..3}.png` | 16×44 |
| Boss rocket | `enemies/missile.png` | 24×48 |

### Explosions

| Entity | Subdir | Frames | Render size |
|--------|--------|--------|-------------|
| Scout | `explosions/fx2/` | 11 | 80×80 |
| Fighter | `explosions/ship1/` | 10 | 80×80 |
| Kamikaze | `explosions/fx3/` | 11 | 80×80 |
| Gunner | `explosions/ship2/` | 12 | 80×80 |
| Striker | `explosions/ship3/` | 11 | 80×80 |
| Interceptor | `explosions/ship4/` | 11 | 80×80 |
| Boss | `explosions/ship6/` | 11 | 160×160 |
| Player | `explosions/ship5/` | 11 | 80×80 |

### Power-ups

| Power-up | Path |
|----------|------|
| Rapid fire | `powerups/rapid_fire.png` |
| Shield | `powerups/shield.png` |
| Gun upgrade | `powerups/gun_upgrade.png` |
| Rocket | `powerups/rocket.png` |
| Extra life | `powerups/extra_life.png` |

### Background

| Asset | Path | Native size |
|-------|------|-------------|
| Background tile | `bg/bg.png` | 700×800 (scaled to fit SCREEN_W) |

## Asset pipeline

All sprites loaded via `src.assets.get(path)` (lazy cache, `pygame.Surface`). Scaling happens per-entity at construction time via `pygame.transform.scale`.

| Directory | Naming | Animation |
|-----------|--------|-----------|
| `player/` | `{pose}.png`, `shadow_{pose}.png` | 5 directional poses via lerp |
| `enemies/` | `{name}.png`, `boss{n}.png` | None (static) |
| `enemy_fx/` | `{type}_{frame}.png` | 2–3 frame loops, 80 ms/frame |
| `explosions/` | `{Set}_{frame}.png` | 10–12 frame sequences, 55 ms/frame |
| `powerups/` | `{name}.png` | None (static) |
| `Shots/` | `shot{n}_{phase}_{frame}.png` | Launch → Travel → Impact |

## Per-directory docs

| Directory | Doc |
|-----------|-----|
| `Shots/` | `Shots/SPRITES.md` |
| All others | *(no separate doc — see this file)* |
