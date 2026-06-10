EXPLOSION_W = 80
EXPLOSION_H = 80
EXPLOSION_W_BOSS = 160
EXPLOSION_H_BOSS = 160
EXPLOSION_FRAME_MS = 55

EXPLOSION_FRAMES = [
    f"enemy_explosions/Explosion1/Explosion1_{i}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_2 = [
    f"enemy_explosions/Explosion2/Explosion2_{i}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_3 = [
    f"enemy_explosions/Explosion3/Explosion3_{i}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP1 = [
    f"enemy_explosions/Ship1_Explosion/Ship1_Explosion_{i:03d}.png" for i in range(1, 11)
]
EXPLOSION_FRAMES_SHIP2 = [
    f"enemy_explosions/Ship2_Explosion/Ship2_Explosion_{i:03d}.png" for i in range(1, 13)
]
EXPLOSION_FRAMES_SHIP3 = [
    f"enemy_explosions/Ship3_Explosion/Ship3_Explosion_{i:03d}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP4 = [
    f"enemy_explosions/Ship4_Explosion/Ship4_Explosion_{i:03d}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP5 = [
    f"enemy_explosions/Ship5_Explosion/Ship5_Explosion_{i:03d}.png" for i in range(1, 12)
]
EXPLOSION_FRAMES_SHIP6 = [
    f"enemy_explosions/Ship6_Explosion/Ship6_Explosion_{i:03d}.png" for i in range(1, 12)
]

EXPL_SCOUT = EXPLOSION_FRAMES_2
EXPL_KAMIKAZE = EXPLOSION_FRAMES_3
EXPL_FIGHTER = EXPLOSION_FRAMES_SHIP1
EXPL_GUNNER = EXPLOSION_FRAMES_SHIP2
EXPL_STRIKER = EXPLOSION_FRAMES_SHIP3
EXPL_INTERCEPTOR = EXPLOSION_FRAMES_SHIP4
EXPL_BOSS = EXPLOSION_FRAMES_SHIP6
EXPL_PLAYER = EXPLOSION_FRAMES_SHIP5
