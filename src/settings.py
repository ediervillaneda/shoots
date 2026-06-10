SCREEN_W = 540
SCREEN_H = 960
FPS = 60
TITLE = "Starfall"

# Player
PLAYER_SPEED = 300  # px/s (≈5 px/frame a 60fps)
PLAYER_COLOR = (100, 180, 255)
PLAYER_W = 40
PLAYER_H = 50

# Bullet
BULLET_SPEED = 720  # px/s (≈12 px/frame a 60fps)
BULLET_DAMAGE = 1
BULLET_COLOR = (255, 255, 100)
BULLET_W = 6
BULLET_H = 14
BULLET_COOLDOWN = 250  # ms entre disparos

# Scout
SCOUT_SPEED = 180
SCOUT_COLOR = (220, 50, 50)
SCOUT_W = 40
SCOUT_H = 40
SCOUT_HP = 1
SCOUT_POINTS = 100

# Fighter
FIGHTER_SPEED = 120
FIGHTER_COLOR = (220, 140, 50)
FIGHTER_W = 44
FIGHTER_H = 44
FIGHTER_HP = 2
FIGHTER_POINTS = 250
FIGHTER_AMPLITUDE = 80
FIGHTER_FREQUENCY = 1.25

# Lives & invincibility
PLAYER_LIVES = 3
INVINCIBILITY_MS = 2000

# HUD
HUD_FONT_SIZE = 24
HUD_COLOR = (255, 255, 255)
HUD_MARGIN = 10

# Enemy bullet
ENEMY_BULLET_SPEED = 300  # px/s
ENEMY_BULLET_DAMAGE = 1
ENEMY_BULLET_COLOR = (255, 80, 80)
ENEMY_BULLET_W = 6
ENEMY_BULLET_H = 12

# Fighter shoot
FIGHTER_SHOOT_INTERVAL = 2000  # ms entre disparos por Fighter

# Waves
WAVE_TIME_THRESHOLD = 30_000  # ms para subir oleada (oleadas 0-2)
WAVE_KILL_THRESHOLD = 10  # kills para subir oleada (oleada 3+)
WAVE_SPEED_FACTOR = 0.2  # px/s extra por oleada
WAVE_SPAWN_MIN = 1500  # ms spawn interval en oleada 0
WAVE_SPAWN_MIN_CAP = 600  # mínimo spawn interval
WAVE_FIGHTER_BASE = 30  # % probabilidad Fighter en oleada 0
WAVE_FIGHTER_INC = 10  # % adicional por oleada
WAVE_FIGHTER_CAP = 80  # % máximo Fighter
WAVE_SPAWN_DEC = 150  # ms reduction per wave

# Kamikaze
KAMIKAZE_SPEED = 200
KAMIKAZE_W = 48
KAMIKAZE_H = 48
KAMIKAZE_HP = 2
KAMIKAZE_POINTS = 500

# Gunner — straight down + 3-bullet spread, wave 3+
GUNNER_SPEED = 110
GUNNER_W = 52
GUNNER_H = 52
GUNNER_HP = 5
GUNNER_POINTS = 600
GUNNER_SHOOT_INTERVAL = 2200  # ms
GUNNER_SPREAD_ANGLE = 20       # degrees per side bullet

# Striker — diagonal entry + aimed bursts, wave 6+
STRIKER_SPEED = 210
STRIKER_W = 56
STRIKER_H = 56
STRIKER_HP = 8
STRIKER_POINTS = 1000
STRIKER_SHOOT_INTERVAL = 1500  # ms
STRIKER_ENTRY_Y = 260          # Y past which diagonal becomes straight-down

# Interceptor — fast entry → patrol + rapid fire, wave 10+
INTERCEPTOR_SPEED = 260
INTERCEPTOR_W = 60
INTERCEPTOR_H = 60
INTERCEPTOR_HP = 15
INTERCEPTOR_POINTS = 1500
INTERCEPTOR_SHOOT_INTERVAL = 700   # ms
INTERCEPTOR_Y_TARGET = 170         # Y where patrol begins
INTERCEPTOR_PATROL_SPEED = 190     # px/s horizontal

# Kamikaze wave scaling
WAVE_KAMIKAZE_BASE = 10  # % probability at wave 0
WAVE_KAMIKAZE_INC = 5    # % added per wave
WAVE_KAMIKAZE_CAP = 40   # % maximum

# New enemies wave scaling
WAVE_GUNNER_MIN_WAVE = 3
WAVE_GUNNER_BASE = 25
WAVE_GUNNER_INC = 5
WAVE_GUNNER_CAP = 50

WAVE_STRIKER_MIN_WAVE = 6
WAVE_STRIKER_BASE = 20
WAVE_STRIKER_INC = 5
WAVE_STRIKER_CAP = 40

WAVE_INTERCEPTOR_MIN_WAVE = 10
WAVE_INTERCEPTOR_BASE = 15
WAVE_INTERCEPTOR_INC = 5
WAVE_INTERCEPTOR_CAP = 35

# Power-ups
POWERUP_SPEED = 150  # px/s downward
POWERUP_W = 32
POWERUP_H = 32
POWERUP_DROP_CHANCE = 0.20  # 20% per kill
PLAYER_LIVES_MAX = 5
RAPIDFIRE_COOLDOWN_MULT = 0.4  # BULLET_COOLDOWN × 0.4 with RapidFire active

# Sprites
SPRITE_SCOUT = "enemy_ships/Ship1/Ship1.png"
SPRITE_SHIP = "enemy_boss/Ship_1_D.png"
SPRITE_PLASMA = "ship/plasm.png"
SPRITE_ROCKET = "enemy_boss/Missile_A.png"
SPRITE_FIGHTER = "enemy_ships/Ship2/Ship2.png"
SPRITE_FIGHTER_BULLET = "ship/bullet-1.png"
SPRITE_KAMIKAZE = "enemy_ships/Ship3/Ship3.png"
SPRITE_GUNNER = "enemy_ships/Ship4/Ship4.png"
SPRITE_STRIKER = "enemy_ships/Ship5/Ship5.png"
SPRITE_INTERCEPTOR = "enemy_ships/Ship6/Ship6.png"
SPRITE_KAMIKAZE_BULLET = "ship/bullet-2.png"
SPRITE_SHIELD_OVERLAY = "ship/shield.png"
SPRITE_PU_RAPID_FIRE = "ship/bonus_time.png"
SPRITE_PU_SHIELD = "ship/bonus_shield.png"
SPRITE_PU_DOUBLE_SHOT = "ship/bonus_gun.png"
SPRITE_PU_TRIPLE_SHOT = "ship/bonus_gun.png"
SPRITE_PU_ROCKET = "ship/bonus_rocket.png"
SPRITE_PU_EXTRA_LIFE = "ship/bonus_life.png"

# Shot sprites (from assets/Shots/)
SPRITE_SHOT1 = "Shots/Shot1/shot1_4.png"
SPRITE_SHOT2 = "Shots/Shot2/shot2_4.png"
SPRITE_SHOT3 = "Shots/Shot3/shot3_asset.png"
SPRITE_SHOT4 = "Shots/Shot4/shot4_asset.png"
SPRITE_SHOT5 = "Shots/Shot5/shot5_asset.png"
SPRITE_SHOT6 = "Shots/Shot6/shot6_asset.png"

SHOT_LEVEL_MAX = 6

# Bullet sizes per shot level
BULLET_W_L1 = 50
BULLET_H_L1 = 50
BULLET_W_L2 = 75
BULLET_H_L2 = 75
BULLET_W_L3 = 75
BULLET_H_L3 = 75
BULLET_W_L4 = 80
BULLET_H_L4 = 80
BULLET_W_L5 = 85
BULLET_H_L5 = 85
BULLET_W_L6 = 90
BULLET_H_L6 = 90

# Boss
BOSS_W = 96
BOSS_H = 80
BOSS_HP = 30
BOSS_POINTS = 5000
BOSS_COLOR = (180, 50, 180)  # fallback color (sprite used in production)
BOSS_SPEED = 150  # px/s
BOSS_Y_TARGET = 120  # Y donde termina entrada y empieza ping-pong
BOSS_SHOOT_INTERVAL_P1 = 1500  # ms fase 1 (single shot)
BOSS_SHOOT_INTERVAL_P2 = 1000  # ms fase 2 (spread)
BOSS_SPREAD_ANGLE = 20  # grados desde vertical
BOSS_HEALTH_BAR_H = 12
BOSS_BAR_Y_OFFSET = 6  # px gap between score row and boss health bar
BOSS_WAVE_INTERVAL = 10  # waves entre apariciones del boss
BOSS_SPRITES = [
    "enemy_boss/Enemy_1_A.png",
    "enemy_boss/Enemy_2_A.png",
    "enemy_boss/Enemy_3_A.png",
    "enemy_boss/Enemy_4_A.png",
]
BOSS_SPRITES_FIXED_COUNT = 3  # primeras 3 apariciones ordenadas, luego aleatorio

# Rocket (player weapon)
ROCKET_SPEED = 500
ROCKET_W = 24
ROCKET_H = 48
ROCKET_DAMAGE = 5
ROCKET_AREA_DAMAGE = 2
ROCKET_RADIUS = 90
ROCKET_COOLDOWN = 1000  # ms entre cohetes
ROCKET_ANGLE_DEG = 20.0  # ángulo desde la vertical para rockets laterales
ROCKET_MAX_COUNT = 2     # máximo rockets simultáneos

# Explosion
EXPLOSION_W = 80
EXPLOSION_H = 80
EXPLOSION_W_BOSS = 160
EXPLOSION_H_BOSS = 160
EXPLOSION_FRAME_MS = 55  # ms por frame (11 frames ≈ 600 ms total)
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
    f"enemy_explosions/Ship1_Explosion/Ship1_Explosion_{n}.png"
    for n in ["001", "003", "008", "009", "012", "013", "014", "017", "019", "020"]
]
EXPLOSION_FRAMES_SHIP2 = [
    f"enemy_explosions/Ship2_Explosion/Ship2_Explosion_{n}.png"
    for n in [
        "000",
        "004",
        "005",
        "008",
        "009",
        "010",
        "013",
        "014",
        "015",
        "016",
        "019",
        "021",
    ]
]
EXPLOSION_FRAMES_SHIP3 = [
    f"enemy_explosions/Ship3_Explosion/Ship3_Explosion_{n}.png"
    for n in [
        "000",
        "004",
        "005",
        "007",
        "009",
        "012",
        "013",
        "015",
        "018",
        "019",
        "021",
    ]
]
EXPLOSION_FRAMES_SHIP4 = [
    f"enemy_explosions/Ship4_Explosion/Ship4_Explosion_{n}.png"
    for n in [
        "000",
        "003",
        "005",
        "007",
        "008",
        "012",
        "013",
        "015",
        "018",
        "019",
        "020",
    ]
]
EXPLOSION_FRAMES_SHIP5 = [
    f"enemy_explosions/Ship5_Explosion/Ship5_Explosion_{n}.png"
    for n in [
        "001",
        "003",
        "006",
        "007",
        "008",
        "011",
        "013",
        "014",
        "017",
        "019",
        "020",
    ]
]
EXPLOSION_FRAMES_SHIP6 = [
    f"enemy_explosions/Ship6_Explosion/Ship6_Explosion_{n}.png"
    for n in [
        "000",
        "004",
        "005",
        "007",
        "009",
        "011",
        "013",
        "016",
        "017",
        "019",
        "021",
    ]
]

# Entity-specific explosion assignments
EXPL_SCOUT = EXPLOSION_FRAMES_2        # small energy burst
EXPL_KAMIKAZE = EXPLOSION_FRAMES_3     # small energy burst (variant)
EXPL_FIGHTER = EXPLOSION_FRAMES_SHIP1  # medium ship explosion
EXPL_GUNNER = EXPLOSION_FRAMES_SHIP2   # medium ship explosion (variant)
EXPL_STRIKER = EXPLOSION_FRAMES_SHIP3  # larger ship explosion
EXPL_INTERCEPTOR = EXPLOSION_FRAMES_SHIP4  # large ship explosion
EXPL_BOSS = EXPLOSION_FRAMES_SHIP6     # large ship explosion
EXPL_PLAYER = EXPLOSION_FRAMES_SHIP5   # player ship explosion
