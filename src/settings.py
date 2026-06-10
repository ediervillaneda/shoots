SCREEN_W = 540
SCREEN_H = 960
FPS = 60
TITLE = "Starfall"

# Player
PLAYER_SPEED = 300      # px/s (≈5 px/frame a 60fps)
PLAYER_COLOR = (100, 180, 255)
PLAYER_W = 40
PLAYER_H = 50

# Bullet
BULLET_SPEED = 720      # px/s (≈12 px/frame a 60fps)
BULLET_DAMAGE = 1
BULLET_COLOR = (255, 255, 100)
BULLET_W = 6
BULLET_H = 14
BULLET_COOLDOWN = 250   # ms entre disparos

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

# Spawning
SPAWN_INTERVAL = 1500

# Lives & invincibility
PLAYER_LIVES     = 5
INVINCIBILITY_MS = 2000

# HUD
HUD_FONT_SIZE = 24
HUD_COLOR     = (255, 255, 255)
HUD_MARGIN    = 10

# Enemy bullet
ENEMY_BULLET_SPEED  = 300       # px/s
ENEMY_BULLET_DAMAGE = 1
ENEMY_BULLET_COLOR  = (255, 80, 80)
ENEMY_BULLET_W      = 6
ENEMY_BULLET_H      = 12

# Fighter shoot
FIGHTER_SHOOT_INTERVAL = 2000   # ms entre disparos por Fighter

# Waves
WAVE_TIME_THRESHOLD  = 30_000   # ms para subir oleada (oleadas 0-2)
WAVE_KILL_THRESHOLD  = 10       # kills para subir oleada (oleada 3+)
WAVE_SPEED_FACTOR    = 0.2      # px/s extra por oleada
WAVE_SPAWN_MIN       = 1500     # ms spawn interval en oleada 0
WAVE_SPAWN_MIN_CAP   = 600      # mínimo spawn interval
WAVE_FIGHTER_BASE    = 30       # % probabilidad Fighter en oleada 0
WAVE_FIGHTER_INC     = 10       # % adicional por oleada
WAVE_FIGHTER_CAP     = 80       # % máximo Fighter
