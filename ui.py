# ui.py

import pygame as pg
from settings import *
import math

# Store popups globally within this module or pass around
score_popups = []
popup_frame_count = 0

# Removed achievement notifications list and functions
# achievement_notifications = []
# NOTIFICATION_DURATION = 4.0

def draw_text(surface, text, size, x, y, color, font, align="center"):
    """Helper function to draw text with alignment."""
    if not font: # Basic fallback if font loading failed
        font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "topright":
        text_rect.topright = (x, y)
    elif align == "midbottom":
        text_rect.midbottom = (x, y)
    elif align == "midtop":
        text_rect.midtop = (x, y)
    elif align == "midleft":
        text_rect.midleft = (x,y)
    elif align == "midright":
        text_rect.midright = (x,y)
    surface.blit(text_surface, text_rect)
    return text_rect

def add_score_popup(position, text="+1", color=YELLOW, assets=None):
    """Adds a score popup effect."""
    global popup_frame_count
    if assets and assets.font_tiny:
        text_surf = assets.font_tiny.render(text, True, color)
        rect = text_surf.get_rect(center=position)
        # Store creation time using Pygame ticks for time-based duration
        score_popups.append([text_surf, rect, pg.time.get_ticks()])

def update_and_draw_popups(surface, dt):
    """Updates and draws score popups based on time."""
    current_time = pg.time.get_ticks()
    active_popups = []
    # Convert POPUP_DURATION_FRAMES to milliseconds
    popup_duration_ms = POPUP_DURATION_FRAMES * (1000.0 / FPS)

    for popup in score_popups:
        text_surf, rect, creation_time = popup
        elapsed_time = current_time - creation_time

        if elapsed_time < popup_duration_ms:
            # Move up based on dt for smooth animation
            rect.y -= POPUP_SPEED * dt * 60 # Scale speed by FPS if constant is frame-based

            # Calculate alpha based on time elapsed
            alpha = max(0, 255 * (1 - (elapsed_time / popup_duration_ms)))
            text_surf.set_alpha(int(alpha))
            surface.blit(text_surf, rect)
            active_popups.append(popup)
    score_popups[:] = active_popups

def clear_popups():
    """Clears the list of active score popups."""
    global score_popups
    score_popups.clear()

# --- Removed Achievement Notification functions ---
# def add_achievement_notification(...)
# def update_and_draw_notifications(...)
# def clear_notifications(...)

# ui.py
# ... (imports and other functions like draw_text, popups) ...

def draw_hud(surface, score, high_score, powerup_timer, powerup_type, assets): # Keep args for now, ignore last two
    """Draws the minimalistic Heads Up Display."""
    # Score Top Left
    draw_text(surface, f"Score: {score}", 30, 15, 15, WHITE, assets.font_small, align="topleft")
    # High Score Top Right
    draw_text(surface, f"Best: {high_score}", 30, SCREEN_WIDTH - 15, 15, GRAY, assets.font_small, align="topright")
    # --- Removed Powerup Timer Display ---

# ... (rest of ui.py, ensuring draw_main_menu, draw_game_over, draw_pause etc are the simplified versions) ...
# Make sure draw_main_menu/draw_game_over/draw_pause don't reference removed features/states.

def draw_main_menu(surface, highscore, assets):
    """Draws the minimalistic Main Menu."""
    assets.draw_background(surface) # Draw gradient
    title_font = assets.font_normal if assets.font_normal else pg.font.SysFont(None, 70)
    option_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 40)
    info_font = assets.font_tiny if assets.font_tiny else pg.font.SysFont(None, 25)

    # Game Title
    draw_text(surface, TITLE, 70, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.25, YELLOW, title_font, align="center")

    # High Score
    draw_text(surface, f"High Score: {highscore}", 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.45, WHITE, option_font, align="center")

    # Options
    menu_y_start = SCREEN_HEIGHT * 0.60
    line_height = 55
    draw_text(surface, "[ ENTER ] Start Game", 35, SCREEN_WIDTH // 2, menu_y_start, GRAY, option_font, align="center")
    draw_text(surface, f"[ {pg.key.name(FULLSCREEN_TOGGLE_KEY).upper()} ] Toggle Fullscreen", 30, SCREEN_WIDTH // 2, menu_y_start + line_height, GRAY, info_font, align="center")
    draw_text(surface, "[ Q ] Quit Game", 35, SCREEN_WIDTH // 2, menu_y_start + line_height * 2, GRAY, option_font, align="center")

    # Basic Controls Info
    controls_text = "Controls: LEFT/RIGHT Arrows | UP/SPACE = Jump | P = Pause"
    draw_text(surface, controls_text, 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, LIGHT_GRAY, info_font, align="center")

def draw_game_over(surface, score, highscore, new_highscore, assets):
    """Draws the minimalistic Game Over screen."""
    assets.draw_background(surface) # Keep background consistent or make it darker
    overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Dark overlay
    surface.blit(overlay, (0,0))

    title_font = assets.font_normal if assets.font_normal else pg.font.SysFont(None, 70)
    score_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 45)
    info_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 35)

    # Game Over Text
    draw_text(surface, "Game Over", 70, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.25, RED, title_font, align="center")

    # Score Display
    y_start = SCREEN_HEIGHT * 0.45
    if new_highscore:
         draw_text(surface, "New High Score!", 35, SCREEN_WIDTH // 2, y_start - 40, GOLD, info_font, align="center")
    draw_text(surface, f"Score: {score}", 45, SCREEN_WIDTH // 2, y_start, WHITE, score_font, align="center")
    draw_text(surface, f"Best: {highscore}", 35, SCREEN_WIDTH // 2, y_start + 50, YELLOW, info_font, align="center")

    # Options
    option_y = SCREEN_HEIGHT * 0.75
    option_spacing = 150
    draw_text(surface, "[ R ] Replay", 35, SCREEN_WIDTH // 2 - option_spacing, option_y, GRAY, info_font, align="center")
    draw_text(surface, "[ M ] Menu", 35, SCREEN_WIDTH // 2 , option_y, GRAY, info_font, align="center")
    draw_text(surface, "[ Q ] Quit", 35, SCREEN_WIDTH // 2 + option_spacing, option_y, GRAY, info_font, align="center")


def draw_pause_screen(surface, assets):
    """Draws the minimalistic Pause screen."""
    overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) # Darker overlay for pause
    surface.blit(overlay, (0,0))

    title_font = assets.font_normal if assets.font_normal else pg.font.SysFont(None, 60)
    info_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 35)

    draw_text(surface, "Paused", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.3, YELLOW, title_font, align="center")

    option_y = SCREEN_HEIGHT * 0.55
    line_height = 50
    draw_text(surface, "[ P ] Resume", 35, SCREEN_WIDTH // 2, option_y, WHITE, info_font, align="center")
    draw_text(surface, "[ M ] Main Menu", 35, SCREEN_WIDTH // 2, option_y + line_height, WHITE, info_font, align="center")
    draw_text(surface, "[ Q ] Quit Game", 35, SCREEN_WIDTH // 2, option_y + line_height * 2, WHITE, info_font, align="center")

# --- Removed draw_tutorial ---
# --- Removed draw_achievements_screen ---

def draw_transition(surface, direction="in", progress=0.0, color=BLACK):
    """Draws a fade transition."""
    if progress <= 0: return
    progress = max(0.0, min(1.0, progress)) # Clamp progress

    overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)
    alpha = int(255 * progress) if direction == "in" else int(255 * (1.0 - progress))
    overlay.fill(color + (alpha,)) # Add alpha to color tuple
    surface.blit(overlay, (0,0))