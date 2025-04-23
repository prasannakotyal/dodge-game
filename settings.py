# settings.py

import pygame as pg

# --- Core Settings ---
TITLE = "Simple Dodge"
SCREEN_WIDTH = 600     # Smaller width
SCREEN_HEIGHT = 800    # Smaller height
FPS = 60
GAME_FONT = None
USE_DELTA_TIME = True # Keep for physics if needed, less critical for simple movement

# --- Window Settings ---
WINDOW_FLAGS = pg.RESIZABLE | pg.SCALED
FULLSCREEN_FLAGS = pg.FULLSCREEN | pg.SCALED
DEFAULT_FULLSCREEN = False
FULLSCREEN_TOGGLE_KEY = pg.K_F11

# --- File Paths ---
HIGHSCORE_FILE = "data/game_data.json"
FONT_NAME = pg.font.match_font('arial')
SOUND_DIR = "assets/sounds"
COLLECT_SOUND = "collect.wav"
HIT_SOUND = "hit.wav"
# Removed powerup/levelup sounds if files don't exist
# POWERUP_SOUND = "powerup.wav"
# LEVELUP_SOUND = "levelup.wav"
IMG_DIR = "assets/images"

# --- Player Settings ---
PLAYER_BASE = 55       # Increased base width
PLAYER_HEIGHT = 45     # Increased height
PLAYER_SPEED = 8.5
PLAYER_GRAVITY = 0.7
PLAYER_JUMP_POWER = -14
PLAYER_GROUND_Y_OFFSET = 15
PLAYER_START_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - PLAYER_GROUND_Y_OFFSET)
# PLAYER_NEAR_MISS_THRESHOLD = 25 # Removed
# PLAYER_SHIELD_COLOR = (100, 100, 255, 128) # Removed
PLAYER_HIT_FLASH_DURATION = 0.2
# PLAYER_NEAR_MISS_FLASH_DURATION = 0.1 # Removed

# --- Item & Obstacle Settings ---
ITEM_SIZE_COLLECTIBLE = 35
ITEM_SIZE_OBSTACLE = 40
ITEM_SPAWN_BASE_RATE = 30 # Slightly increased rate
# ITEM_SPAWN_RATE_MIN = 15 # Removed (simplifying)
# ITEM_SPAWN_RATE_LEVEL_REDUCTION = 2 # Removed
BLOCK_SPEED_START = 3.5 # Start a bit slower
# SPEED_INCREMENT_PER_LEVEL = 0.5 # Removed
SPEED_INCREMENT_PER_SCORE = 0.07 # How much speed increases per point scored
MAX_ITEM_SPEED = 14.0 # Cap speed increase
COLLECTIBLE_PROBABILITY_BASE = 0.65 # Fixed probability
# COLLECTIBLE_PROBABILITY_MIN = 0.40 # Removed
COLLECTIBLE_PULSE_SPEED = 3
COLLECTIBLE_PULSE_AMOUNT = 0.1

# --- Power-up Settings --- REMOVED ---
# POWERUP_SIZE = 30
# POWERUP_SPAWN_PROBABILITY = 0.05
# POWERUP_DURATION = 8.0
# POWERUP_TYPES = ['shield', 'magnet', 'slowmo', 'multiplier']
# POWERUP_COLORS = { ... }
# POWERUP_MAGNET_RADIUS = 150
# POWERUP_SLOWMO_FACTOR = 0.5
# POWERUP_MULTIPLIER_AMOUNT = 2

# --- Combo System Settings --- REMOVED ---
# COMBO_TIMEOUT = 1.5
# COMBO_SCORE_MULTIPLIER = True
# COMBO_MAX_DISPLAY = 10

# --- Difficulty Settings --- REMOVED (Using score directly) ---
# LEVEL_SCORE_THRESHOLDS = [10, 25, 45, 70, 100, 140, 190, 250]
# LEVEL_MAX = len(LEVEL_SCORE_THRESHOLDS)

# --- Visual & UI Settings ---
BG_COLOR_DARK_START = (10, 10, 25) # Even darker BG
BG_COLOR_LIGHT_START = (25, 25, 50)
# BG_COLOR_CHANGE_RATE = 5 # Keep subtle change? Optional.
POPUP_DURATION_FRAMES = 40 # Shorter popup?
POPUP_SPEED = 1.8
SCORE_MILESTONE = 10 # Keep for subtle feedback maybe
TRANSITION_SPEED = 3
SCREEN_SHAKE_DURATION = 0.15
SCREEN_SHAKE_INTENSITY = 4

# --- Colors --- (Keep as is)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
# BLUE = (100, 100, 255) # Original Blue
# BLUE = (0, 180, 255)   # Brighter Cyan-Blue Option
BLUE = (255, 255, 255) # *** White Player - High Contrast ***
YELLOW = (255, 255, 0)
GRAY = (180, 180, 180)
LIGHT_GRAY = (120, 120, 120)
GOLD = (255, 215, 0)

# --- Game States (Simplified) ---
STATE_MENU = 0
STATE_GAME = 2
STATE_PAUSED = 3
STATE_GAMEOVER = 4
STATE_TRANSITION_IN = 6
STATE_TRANSITION_OUT = 7

# --- Achievements (Keep data structure for persistence, but ignore in gameplay) ---
ACHIEVEMENTS = { ... } # Keep as is

# --- Derived/Calculated Settings (Ensure these are at the END) ---
# Recalculate ground Y based on potentially changed screen/player height
PLAYER_GROUND_Y = SCREEN_HEIGHT - PLAYER_HEIGHT - PLAYER_GROUND_Y_OFFSET
# Recalculate start position based on potentially changed screen width and ground Y
PLAYER_START_POS = (SCREEN_WIDTH // 2, PLAYER_GROUND_Y) # Place mid-bottom using ground Y