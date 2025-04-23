# persistence.py

import json
import os
from settings import * # Import needed settings

class Persistence:
    def __init__(self):
        self.data = {
            "highscore": 0,
            "sound_enabled": True,
            "fullscreen": DEFAULT_FULLSCREEN, # Add fullscreen preference
            # "played_before": False, # Removed if tutorial is gone
            "stats": {
                "games_played": 0,
                "total_collectibles": 0,
                "total_score": 0,
                "max_combo": 0, # Keep for potential future use
                "game_near_misses": 0, # Keep stat tracking
            },
            # "achievements": {aid: data['unlocked'] for aid, data in ACHIEVEMENTS.items()} # Removed achievements save
        }
        # Ensure directory exists
        save_dir = os.path.dirname(HIGHSCORE_FILE)
        if save_dir and not os.path.exists(save_dir):
             os.makedirs(save_dir)
        self.load_data()

    def load_data(self):
        if not os.path.exists(HIGHSCORE_FILE):
            print("No save file found, using defaults.")
            self.save_data() # Create file with defaults
            return

        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                loaded_data = json.load(f)

            # Validate and merge loaded data
            self.data["highscore"] = int(loaded_data.get("highscore", 0))
            self.data["sound_enabled"] = bool(loaded_data.get("sound_enabled", True))
            self.data["fullscreen"] = bool(loaded_data.get("fullscreen", DEFAULT_FULLSCREEN)) # Load fullscreen setting
            # self.data["played_before"] = bool(loaded_data.get("played_before", False)) # Removed

            # Load stats safely
            loaded_stats = loaded_data.get("stats", {})
            for key in self.data["stats"]:
                if key in loaded_stats and isinstance(loaded_stats[key], (int, float)):
                     self.data["stats"][key] = loaded_stats[key]

            # Removed achievement loading
            # loaded_achievements = loaded_data.get("achievements", {}) ...

            print("Game data loaded successfully.")

        except (IOError, json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"Error loading game data: {e}. Using default values.")
            # Reset to defaults if loading fails
            default_fullscreen = self.data["fullscreen"] # Preserve attempt if possible
            self.__init__() # Re-initialize with defaults
            self.data["fullscreen"] = default_fullscreen # Restore loaded fullscreen if possible
            self.save_data()

    def save_data(self):
        try:
            # Update achievement status before saving - Removed
            # self.data["achievements"] = {aid: data['unlocked'] for aid, data in ACHIEVEMENTS.items()}

            with open(HIGHSCORE_FILE, 'w') as f:
                json.dump(self.data, f, indent=4)
            # print("Game data saved.") # Can be noisy
        except IOError as e:
            print(f"Error saving game data: {e}")

    def get_highscore(self):
        return self.data["highscore"]

    def set_highscore(self, score):
        if score > self.data["highscore"]:
            self.data["highscore"] = score
            # Don't save here automatically, save usually happens at end of game or quit
            # self.save_data()
            return True
        return False

    def is_sound_enabled(self):
        return self.data["sound_enabled"]

    def toggle_sound(self):
        self.data["sound_enabled"] = not self.data["sound_enabled"]
        self.save_data() # Save immediately on toggle is fine

    def is_fullscreen(self): # Added getter
        return self.data.get("fullscreen", DEFAULT_FULLSCREEN)

    def set_fullscreen(self, fullscreen_state): # Added setter
        self.data["fullscreen"] = bool(fullscreen_state)
        self.save_data() # Save immediately on toggle

    # Removed played_before methods

    def increment_stat(self, stat_name, value=1):
        if stat_name in self.data["stats"]:
            self.data["stats"][stat_name] += value
        else:
            print(f"Warning: Tried to increment unknown stat '{stat_name}'")

    def get_stat(self, stat_name):
        return self.data["stats"].get(stat_name, 0)

  