# Shot Sprite Animation Guide

Each Shot directory contains three phases of the bullet lifecycle:

## Phase 1: Launch (`shotX_1.png` → `shotX_N.png`)

Played once when the bullet leaves the player's ship. Cycles through frames 1..N to create a muzzle-flash / spawn animation, then transitions to the travel sprite.

## Phase 2: Travel (`shotX_asset.png`)

The single static sprite displayed while the bullet flies across the screen toward enemies. This is what the player sees during normal gameplay.

## Phase 3: Impact (`shotX_expN.png`)

Played when the bullet hits an enemy. Each shot type has a unique explosion animation with varying frame counts.

---

## Shot inventory

| Shot | Launch frames | Travel sprite | Impact frames | Source size |
|------|--------------|---------------|---------------|-------------|
| Shot1 | `shot1_1` … `shot1_4` (4) | `shot1_asset.png` | `shot1_exp1` … `shot1_exp5` (5) | 32×32 |
| Shot2 | `shot2_1` … `shot2_6` (6) | `shot2_asset.png` | `shot2_exp1` … `shot2_exp5` (5) | 64×64 |
| Shot3 | `shot3_1` … `shot3_3` (3) | `shot3_asset.png` | `shot3_exp1` … `shot3_exp4` (4) | 64×64 |
| Shot4 | `shot4_1` … `shot4_5` (5) | `shot4_asset.png` | `shot4_exp1` … `shot4_exp8` (8) | 64×64 |
| Shot5 | `shot5_1` … `shot5_5` (5) | `shot5_asset.png` | `shot5_exp1` … `shot5_exp8` (8) | 128×128 |
| Shot6 | `shot6_1` … `shot6_4` (4) | `shot6_asset.png` | `shot6_exp1` … `shot6_exp10` (10) | 128×128 |

## Usage in game

Currently `Shot1`, `Shot2`, and `Shot4` are used for player bullets at different shot levels:

| Level | Sprite | Display size |
|-------|--------|-------------|
| 1 | `Shots/Shot1/shot1_4.png` | 50×50 |
| 2 | `Shots/Shot2/shot2_4.png` | 75×75 |
| 3 | `Shots/Shot4/shot4_asset.png` | 80×80 |

Shot3, Shot5, and Shot6 are available for future use (enemy bullets, rocket alt-fire, boss weapons, etc.).

## Notes

- All sprite directories are flat (no subdirectories).
- All shots follow the same convention: impact frames are numbered `exp1`…`expN`.
- The `_asset.png` files are typically the largest / most detailed frame and are safe to use as a static sprite.
