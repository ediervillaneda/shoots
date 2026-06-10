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

# Kamikaze wave scaling
WAVE_KAMIKAZE_BASE = 10  # % probability at wave 0
WAVE_KAMIKAZE_INC = 5  # % added per wave
WAVE_KAMIKAZE_CAP = 40  # % maximum

# Power-ups
POWERUP_SPEED = 150  # px/s downward
POWERUP_W = 32
POWERUP_H = 32
POWERUP_DROP_CHANCE = 0.20  # 20% per kill
PLAYER_LIVES_MAX = 5
RAPIDFIRE_COOLDOWN_MULT = 0.4  # BULLET_COOLDOWN × 0.4 with RapidFire active

# Sprites
SPRITE_SHIP = "ship/SpaceShip.png"
SPRITE_PLASMA = "ship/plasm.png"
SPRITE_ROCKET = "ship/rocket.png"
SPRITE_FIGHTER = "ship/insect-1.png"
SPRITE_FIGHTER_BULLET = "ship/bullet-1.png"
SPRITE_KAMIKAZE = "ship/insect-2.png"
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
SPRITE_SHOT4 = "Shots/Shot4/shot4_asset.png"

# Bullet sizes per shot level
BULLET_W_L1 = 50
BULLET_H_L1 = 50
BULLET_W_L2 = 75
BULLET_H_L2 = 75
BULLET_W_L3 = 80
BULLET_H_L3 = 80

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
BOSS_BAR_Y_OFFSET = 6   # px gap between score row and boss health bar
BOSS_TRIGGER_MS = 120_000  # ms hasta primer boss (2 min)
BOSS_SPRITES = [
    "enemy/Enemy_1_A.png",
    "enemy/Enemy_2_A.png",
    "enemy/Enemy_3_A.png",
    "enemy/Enemy_4_A.png",
]
BOSS_SPRITES_FIXED_COUNT = 3  # primeras 3 apariciones ordenadas, luego aleatorio
