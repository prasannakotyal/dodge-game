# assets.py

import pygame as pg
import os
# --- Use non-relative import for flat structure ---
from settings import *

class Assets:
    def __init__(self):
        self.sounds = {}
        self.images = {}
        self.font_normal = None
        self.font_small = None
        self.font_tiny = None
        self.sounds_enabled = True
        self.bg_surface = None

    def load(self):
        # Fonts
        try:
            self.font_normal = pg.font.Font(FONT_NAME, 52)
            self.font_small = pg.font.Font(FONT_NAME, 36)
            self.font_tiny = pg.font.Font(FONT_NAME, 24)
            GAME_FONT = self.font_normal # Assign if needed elsewhere, though maybe not now
        except IOError as e:
            print(f"Warning: Could not load font {FONT_NAME}. Using default. Error: {e}")
            self.font_normal = pg.font.SysFont(None, 52)
            self.font_small = pg.font.SysFont(None, 36)
            self.font_tiny = pg.font.SysFont(None, 24)

        # Sounds
        try:
            pg.mixer.init()
            # Load only existing sounds
            self._load_sound(COLLECT_SOUND)
            self._load_sound(HIT_SOUND)
            # --- Removed powerup/levelup sound loading ---
            # self._load_sound(POWERUP_SOUND)
            # self._load_sound(LEVELUP_SOUND)
            print("Sounds loaded.") # Simplified message
        except (pg.error, FileNotFoundError) as e:
            print(f"Warning: Could not initialize mixer or load sounds ({e}). Running without sound.")
            self.sounds_enabled = False

        # Images (Keep placeholder)
        # self._load_image(PLAYER_IMG)

        # Pre-render initial background
        self.update_background(BG_COLOR_DARK_START, BG_COLOR_LIGHT_START)

    def _load_sound(self, filename):
        if not self.sounds_enabled or not filename: return # Added check for empty filename
        path = os.path.join(SOUND_DIR, filename)
        try:
            sound = pg.mixer.Sound(path)
            # Use filename without extension as key
            self.sounds[os.path.splitext(filename)[0]] = sound
        except (pg.error, FileNotFoundError) as e:
            print(f"Warning: Could not load sound '{filename}'. Error: {e}")

    def _load_image(self, filename):
        if not filename: return
        path = os.path.join(IMG_DIR, filename)
        try:
            image = pg.image.load(path).convert_alpha()
            self.images[os.path.splitext(filename)[0]] = image
        except (pg.error, FileNotFoundError) as e:
            print(f"Warning: Could not load image '{filename}'. Error: {e}")

    def play_sound(self, name):
        # Map simplified names to potentially loaded filenames
        sound_key = name # Assume name matches the key used during load
        if self.sounds_enabled and sound_key in self.sounds:
            self.sounds[sound_key].play()

    def get_image(self, name):
        return self.images.get(name, None)

    def update_background(self, color_dark, color_light):
        """Pre-renders the background gradient to a surface."""
        self.bg_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            color = (
                int(color_dark[0] * (1 - color_ratio) + color_light[0] * color_ratio),
                int(color_dark[1] * (1 - color_ratio) + color_light[1] * color_ratio),
                int(color_dark[2] * (1 - color_ratio) + color_light[2] * color_ratio)
            )
            color = tuple(max(0, min(255, c)) for c in color)
            self.bg_surface.fill(color, (0, y, SCREEN_WIDTH, 1))

    def draw_background(self, surface):
        if self.bg_surface:
            surface.blit(self.bg_surface, (0, 0))
        else:
             surface.fill(BG_COLOR_DARK_START)