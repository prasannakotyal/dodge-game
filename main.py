# main.py

import pygame as pg
import sys
import os
# --- Use non-relative imports for flat structure ---
from settings import *
from assets import Assets
from persistence import Persistence
from ui import (draw_main_menu, draw_game_over, draw_pause_screen, draw_transition)
from game import Game

class MainApp:
    def __init__(self):
        pg.init()

        # Initial window setup from persistence
        self.persistence = Persistence() # Init persistence first
        self.fullscreen = self.persistence.is_fullscreen() # Load saved preference
        self.current_flags = FULLSCREEN_FLAGS if self.fullscreen else WINDOW_FLAGS
        resolution = (0,0) if self.fullscreen else (SCREEN_WIDTH, SCREEN_HEIGHT)

        try:
            self.screen = pg.display.set_mode(resolution, self.current_flags)
        except pg.error as e:
            print(f"Error setting initial display mode: {e}. Trying default windowed.")
            self.fullscreen = False
            self.current_flags = WINDOW_FLAGS
            resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
            try:
                 self.screen = pg.display.set_mode(resolution, self.current_flags)
                 self.persistence.set_fullscreen(self.fullscreen) # Save the fallback state
            except Exception as e2:
                 print(f"FATAL ERROR: Could not set any display mode: {e2}")
                 sys.exit()

        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.current_state = STATE_MENU

        # Init other components
        self.assets = Assets()
        self.game = Game(self.screen, self.clock, self.assets, self.persistence)

        # State transition variables
        self.transitioning = False
        self.transition_progress = 0.0
        self.next_state = STATE_MENU
        self.previous_state_for_draw = STATE_MENU
        self.last_score = 0
        self.game_over_is_new_hs = False

        # Load assets and apply settings
        self.assets.load()
        self.assets.sounds_enabled = self.persistence.is_sound_enabled()
        if not self.assets.sounds_enabled:
            if pg.mixer.get_init(): pg.mixer.stop()

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.persistence.set_fullscreen(self.fullscreen)

        if self.fullscreen:
            try:
                info = pg.display.Info()
                resolution = (info.current_w, info.current_h)
                self.current_flags = FULLSCREEN_FLAGS
            except Exception as e:
                 print(f"Error getting display info for fullscreen: {e}. Using default size.")
                 resolution = (SCREEN_WIDTH, SCREEN_HEIGHT) # Fallback
                 self.current_flags = FULLSCREEN_FLAGS
        else: # Switching back to windowed
            self.current_flags = WINDOW_FLAGS
            resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)

        try:
            self.screen = pg.display.set_mode(resolution, self.current_flags)
            self.game.screen = self.screen # Update game's screen ref
        except pg.error as e:
            print(f"Error toggling fullscreen: {e}. Reverting.")
            self.fullscreen = not self.fullscreen # Revert state
            self.persistence.set_fullscreen(self.fullscreen)
            # Attempt to restore previous state
            resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
            self.current_flags = WINDOW_FLAGS
            try:
                 self.screen = pg.display.set_mode(resolution, self.current_flags)
                 self.game.screen = self.screen
            except pg.error as e2:
                 print(f"FATAL ERROR: Could not reset display mode: {e2}")
                 self.running = False # Quit

    def _start_transition(self, next_state):
        if not self.transitioning:
            self.transitioning = True
            self.transition_progress = 0.0
            self.previous_state_for_draw = self.current_state
            self.next_state = next_state

    def _update_transition(self, dt):
        if not self.transitioning: return
        speed = TRANSITION_SPEED
        self.transition_progress += speed * dt
        if self.transition_progress < 1.0 and self.current_state != STATE_TRANSITION_IN:
             self.current_state = STATE_TRANSITION_OUT
        elif self.transition_progress >= 1.0 and self.current_state == STATE_TRANSITION_OUT:
            self.current_state = STATE_TRANSITION_IN
            if self.next_state == STATE_GAME: self.game.reset()
            elif self.next_state == STATE_GAMEOVER:
                 new_hs = self.persistence.set_highscore(self.last_score)
                 self.game_over_is_new_hs = new_hs
            self.transition_progress = 0.0
        elif self.current_state == STATE_TRANSITION_IN:
             if self.transition_progress >= 1.0:
                  self.transition_progress = 1.0
                  self.transitioning = False
                  self.current_state = self.next_state

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000.0
            if delta_time > 0.1: delta_time = 0.1

            self.events()
            if not self.running: break
            self.update(delta_time)
            self.draw()
        self.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: self.running = False; return
            if event.type == pg.VIDEORESIZE and not self.fullscreen: pass # Ignore for SCALED mode
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    if self.current_state in [STATE_MENU, STATE_GAMEOVER, STATE_PAUSED]:
                        self.running = False; return
                if event.key == FULLSCREEN_TOGGLE_KEY: self._toggle_fullscreen()
                if not self.transitioning:
                    if self.current_state == STATE_MENU:
                        if event.key == pg.K_RETURN: self._start_transition(STATE_GAME)
                    elif self.current_state == STATE_GAMEOVER:
                        if event.key == pg.K_r: self._start_transition(STATE_GAME)
                        elif event.key == pg.K_m: self._start_transition(STATE_MENU)

    def update(self, dt):
        if self.transitioning: self._update_transition(dt)

    def draw(self):
        state_to_draw = self.current_state
        if self.transitioning:
            if self.current_state == STATE_TRANSITION_OUT: state_to_draw = self.previous_state_for_draw
            elif self.current_state == STATE_TRANSITION_IN: state_to_draw = self.next_state

        if state_to_draw == STATE_MENU: draw_main_menu(self.screen, self.persistence.get_highscore(), self.assets)
        elif state_to_draw == STATE_GAME:
            if not self.transitioning:
                game_result, score = self.game.run()
                self.last_score = score
                if game_result == "quit": self.running = False
                elif game_result == "menu": self._start_transition(STATE_MENU)
                elif game_result == "gameover": self._start_transition(STATE_GAMEOVER)
            else: self.assets.draw_background(self.screen)
        elif state_to_draw == STATE_GAMEOVER: draw_game_over(self.screen, self.last_score, self.persistence.get_highscore(), self.game_over_is_new_hs, self.assets)
        elif state_to_draw == STATE_PAUSED: pass # Handled in game loop

        if self.transitioning:
            fade_direction = "in" if self.current_state == STATE_TRANSITION_IN else "out"
            draw_transition(self.screen, fade_direction, self.transition_progress)

        pg.display.flip()

    def quit(self):
        try:
            self.persistence.save_data()
        except Exception as e:
            print(f"Error saving data on quit: {e}")
        pg.quit()
        # sys.exit() # Let script end naturally

# --- Entry Point ---
if __name__ == '__main__':
    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("assets/sounds", exist_ok=True)
        os.makedirs("assets/images", exist_ok=True)
        app = MainApp()
        app.run()
    except Exception as e:
        print("\n--- UNHANDLED EXCEPTION IN MAIN ---")
        import traceback
        traceback.print_exc()
        print("------------------------------------\n")
        if pg.get_init(): pg.quit()
        input("--- Press Enter to exit ---")