# Enemy Explosion Animation Guide

Frame-animated sprites played when an enemy or the player is destroyed. Each frame is displayed for `EXPLOSION_FRAME_MS` (55 ms) before advancing; the sprite `kill()`s itself after the last frame.

## Animation lifecycle

Each `Explosion` entity loads all frames at construction, scales them to the target render size, then cycles through them one by one.

## Explosion inventory

| Directory | Frames | Source size | Render size | Used by |
|-----------|--------|-------------|-------------|---------|
| Explosion1/ | `Explosion1_1` … `Explosion1_11` (11) | 128×128 | 80×80 | — |
| Explosion2/ | `Explosion2_1` … `Explosion2_11` (11) | 256×256 | 80×80 | Scout (`EXPL_SCOUT`) |
| Explosion3/ | `Explosion3_1` … `Explosion3_11` (11) | 256×256 | 80×80 | Kamikaze (`EXPL_KAMIKAZE`) |
| Ship1_Explosion/ | 10 frames (sparse IDs) | 128×128 | 80×80 | Fighter (`EXPL_FIGHTER`) |
| Ship2_Explosion/ | 12 frames (sparse IDs) | 128×128 | 80×80 | — |
| Ship3_Explosion/ | 11 frames (sparse IDs) | 256×256 | 80×80 | — |
| Ship4_Explosion/ | 11 frames (sparse IDs) | 256×256 | 80×80 | — |
| Ship5_Explosion/ | 11 frames (sparse IDs) | 256×256 | 80×80 | Player (`EXPL_PLAYER`) |
| Ship6_Explosion/ | 11 frames (sparse IDs) | 256×256 | 160×160 | Boss (`EXPL_BOSS`) |

## Entity-to-explosion mapping

```python
EXPL_SCOUT   = EXPLOSION_FRAMES_2      # Explosion2/        → 80×80
EXPL_KAMIKAZE= EXPLOSION_FRAMES_3      # Explosion3/        → 80×80
EXPL_FIGHTER = EXPLOSION_FRAMES_SHIP1  # Ship1_Explosion/   → 80×80
EXPL_PLAYER  = EXPLOSION_FRAMES_SHIP5  # Ship5_Explosion/   → 80×80
EXPL_BOSS    = EXPLOSION_FRAMES_SHIP6  # Ship6_Explosion/   → 160×160
```

## Frame numbering

- **Explosion1/2/3**: Sequential (`_1` through `_11`).
- **ShipX_Explosion/**: Sparse IDs from the original asset source (e.g. `Ship1_Explosion_001`, `Ship1_Explosion_003`, …). The frame lists in `settings.py` explicitly enumerate only the frames that exist on disk.

## Notes

- All frames for a given explosion are loaded at construction and cached via `src.assets`.
- Total duration: `len(frames) × 55 ms` (≈550–660 ms for 10–12 frames).
- The larger source size (256×256) explosions get downscaled more aggressively; this is fine since they render as pixel art at the target size.
- Unused sets (Explosion1, Ship2, Ship3, Ship4) are available for future enemy types.
