EXPLOSION_W = 80
EXPLOSION_H = 80
EXPLOSION_W_BOSS = 160
EXPLOSION_H_BOSS = 160
EXPLOSION_FRAME_MS = 55

EXPLOSION_FRAMES = [
    f"explosions/fx1/Explosion1_{i}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_2 = [
    f"explosions/fx2/Explosion2_{i}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_3 = [
    f"explosions/fx3/Explosion3_{i}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP1 = [
    f"explosions/ship1/Ship1_Explosion_{i:03d}.png" for i in range(1, 11)
]
EXPLOSION_FRAMES_SHIP2 = [
    f"explosions/ship2/Ship2_Explosion_{i:03d}.png" for i in range(1, 13)
]
EXPLOSION_FRAMES_SHIP3 = [
    f"explosions/ship3/Ship3_Explosion_{i:03d}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP4 = [
    f"explosions/ship4/Ship4_Explosion_{i:03d}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP5 = [
    f"explosions/ship5/Ship5_Explosion_{i:03d}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP6 = [
    f"explosions/ship6/Ship6_Explosion_{i:03d}.png" for i in range(1, 12)
]

EXPL_SCOUT = EXPLOSION_FRAMES_2
EXPL_KAMIKAZE = EXPLOSION_FRAMES_3
EXPL_FIGHTER = EXPLOSION_FRAMES_SHIP1
EXPL_GUNNER = EXPLOSION_FRAMES_SHIP2
EXPL_STRIKER = EXPLOSION_FRAMES_SHIP3
EXPL_INTERCEPTOR = EXPLOSION_FRAMES_SHIP4
EXPL_BOSS = EXPLOSION_FRAMES_SHIP6
EXPL_PLAYER = EXPLOSION_FRAMES_SHIP5
