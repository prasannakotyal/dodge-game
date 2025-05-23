# settings.py

import pygame as pg

# --- Core Settings ---
TITLE = "Dodge Master"
SCREEN_WIDTH = 800     # Increased width for better visibility
SCREEN_HEIGHT = 900    # Increased height for better gameplay
FPS = 60
GAME_FONT = None
USE_DELTA_TIME = True

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
IMG_DIR = "assets/images"

# --- Player Settings ---
PLAYER_BASE = 45       # Slightly smaller for better maneuverability
PLAYER_HEIGHT = 35     # More streamlined
PLAYER_SPEED = 9.0     # Slightly faster for better control
PLAYER_GRAVITY = 0.8   # Slightly stronger gravity
PLAYER_JUMP_POWER = -15 # Stronger jump
PLAYER_GROUND_Y_OFFSET = 20
PLAYER_START_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - PLAYER_GROUND_Y_OFFSET)
PLAYER_HIT_FLASH_DURATION = 0.15

# --- Item & Obstacle Settings ---
ITEM_SIZE_COLLECTIBLE = 30
ITEM_SIZE_OBSTACLE = 35
ITEM_SPAWN_BASE_RATE = 25
BLOCK_SPEED_START = 4.0
SPEED_INCREMENT_PER_SCORE = 0.08
MAX_ITEM_SPEED = 15.0
COLLECTIBLE_PROBABILITY_BASE = 0.60
COLLECTIBLE_PULSE_SPEED = 4
COLLECTIBLE_PULSE_AMOUNT = 0.08

# --- Visual & UI Settings ---
BG_COLOR_DARK_START = (15, 15, 35)    # Darker, more professional blue
BG_COLOR_LIGHT_START = (35, 35, 65)   # Richer gradient
POPUP_DURATION_FRAMES = 35
POPUP_SPEED = 2.0
SCORE_MILESTONE = 10
TRANSITION_SPEED = 3
SCREEN_SHAKE_DURATION = 0.12
SCREEN_SHAKE_INTENSITY = 3

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (100, 150, 255)    # Softer blue for player
YELLOW = (255, 215, 0)    # More golden yellow
GRAY = (180, 180, 180)
LIGHT_GRAY = (120, 120, 120)
GOLD = (255, 215, 0)
ACCENT = (100, 200, 255)  # New accent color for UI elements

# --- Game States ---
STATE_MENU = 0
STATE_GAME = 2
STATE_PAUSED = 3
STATE_GAMEOVER = 4
STATE_TRANSITION_IN = 6
STATE_TRANSITION_OUT = 7

# --- Achievements (Keep data structure for persistence, but ignore in gameplay) ---
ACHIEVEMENTS = { ... } # Keep as is

# --- Derived/Calculated Settings ---
PLAYER_GROUND_Y = SCREEN_HEIGHT - PLAYER_HEIGHT - PLAYER_GROUND_Y_OFFSET
PLAYER_START_POS = (SCREEN_WIDTH // 2, PLAYER_GROUND_Y)