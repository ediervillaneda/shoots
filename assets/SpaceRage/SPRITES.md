# SpaceRage Sprite Pack

Full spritesheet-based asset pack for a space shooter. Includes player ships, enemies, mines, projectiles, explosions, exhaust, shadows, and a background.

## Structure

```
SpaceRage/
├── BG.png                          # Background image (700×800)
├── spritesheet.png                 # TexturePacker spritesheet (502×1005)
├── spritesheet.xml                 # TexturePacker frame data (pivot at 0.5,0.5)
├── stylesheet.png                  # Alternative CSS-layout spritesheet (861×814)
├── stylesheet.txt                  # CSS sprite classes for stylesheet.png
├── Player/                         # 10 sprites, 64×64 each
├── Enemies/                        # 69 sprites (ships + mines)
├── FX/                             # 13 sprites (exhaust + projectiles)
├── Explosions/                     # 29 sprites (3 explosion types)
└── Shadows/                        # 27 sprites (drop shadows)
```

## Player

Two color variants, each with 5 directional poses for strafe/movement animation.

| Variant | Poses | Size |
|---------|-------|------|
| Blue (`b`) | `l1`, `l2`, `m`, `r1`, `r2` | 64×64 |
| Red (`r`) | `l1`, `l2`, `m`, `r1`, `r2` | 64×64 |

Pose naming: `l1`/`l2` = bank left (increasing tilt), `m` = center/neutral, `r1`/`r2` = bank right.

Usage: `player_{color}_{pose}.png`

## Enemies

### Ships

Two ship types, each with 3 color variants and 5 directional poses.

| Ship type | Variants | Poses | Size |
|-----------|----------|-------|------|
| Player 1 | `b` (blue), `g` (green), `r` (red) | `l1`, `l2`, `m`, `r1`, `r2` | 64×64 |
| Player 2 | `b`, `g`, `r` | `l1`, `l2`, `m`, `r1`, `r2` | 64×64 |

Usage: `enemy_{type}_{color}_{pose}.png`

### Mines

Spinning mine variants with animation frames.

| Mine | Frames | Size |
|------|--------|------|
| mine_1 | 01–09 | 48×48 |
| mine_11 | 01–09 | 48×48 |
| mine_12 | 01–09 | 48×48 |
| mine_2 | 01–04 | 48×48 |
| mine_21 | 01–04 | 48×48 |
| mine_22 | 01–04 | 48×48 |

## FX — Exhaust

| Sprite | Size |
|--------|------|
| exhaust_01–05 | 64×64 |

5-frame exhaust/engine glow animation.

## FX — Projectiles

| Weapon | Sprites | Size |
|--------|---------|------|
| Plasma | `plasma_1`, `plasma_2` | 6×21, 5×15 |
| Proton | `proton_01–03` | 13×13, 9×10, 5×5 |
| Vulcan | `vulcan_1–3` | 6×22, 9×22, 4×14 |

## Explosions

3 explosion types with sequential frames.

| Set | Frames | Size |
|-----|--------|------|
| explosion_1 | 01–11 | 52×51 |
| explosion_2 | 01–09 | 52×51 |
| explosion_3 | 01–09 | 52×51 |

## Shadows

Drop-shadow sprites matching the main sprites (same pose structure).

| Shadow set | Count | Size |
|------------|-------|------|
| `enemy_1_shadow` | 5 poses (`l1`–`r2`) | 64×64 |
| `enemy_2_shadow` | 5 poses (`l1`–`r2`) | 64×64 |
| `player_shadow` | 5 poses (`l1`–`r2`) | 64×64 |
| `mine_1_shadow` | 8 frames (`01`–`08`) | 48×48 |
| `mine_2_shadow` | 4 frames (`01`–`04`) | 48×48 |

## Spritesheets

Two spritesheet formats are available:

- **`spritesheet.png`** + **`spritesheet.xml`**: TexturePacker atlas with pivot points at center (0.5, 0.5). Contains every individual sprite in the pack.
- **`stylesheet.png`** + **`stylesheet.txt`**: CSS-sprite layout with pixel-precise background positions. Generated for web/HTML5 export.

## Usage in game

**None.** This pack is not referenced in the codebase. The game currently uses sprites from `enemy_boss/` and `ship/` directories.

## Notes

- All 64×64 sprites share a common pivot at center (0.5, 0.5).
- Explosion frames in the TexturePacker XML show co-linear coordinates across types (explosion_1 and explosion_2 share texture positions in the spritesheet). The loose PNG files in each subdirectory are correct and independent.
- BG.png (700×800) is wider than the game viewport (540×960) — it was designed for a different resolution.
