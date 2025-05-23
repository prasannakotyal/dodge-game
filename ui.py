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

def draw_hud(surface, score, high_score, powerup_timer, powerup_type, assets):
    """Draws the professional Heads Up Display."""
    # Create a semi-transparent background for the score
    score_bg = pg.Surface((200, 40), pg.SRCALPHA)
    score_bg.fill((0, 0, 0, 128))
    surface.blit(score_bg, (10, 10))
    
    # Score with improved styling
    draw_text(surface, f"SCORE: {score}", 28, 110, 30, WHITE, assets.font_small, align="center")
    
    # High Score with improved styling
    high_score_bg = pg.Surface((200, 40), pg.SRCALPHA)
    high_score_bg.fill((0, 0, 0, 128))
    surface.blit(high_score_bg, (SCREEN_WIDTH - 210, 10))
    draw_text(surface, f"BEST: {high_score}", 28, SCREEN_WIDTH - 110, 30, ACCENT, assets.font_small, align="center")

# ... (rest of ui.py, ensuring draw_main_menu, draw_game_over, draw_pause etc are the simplified versions) ...
# Make sure draw_main_menu/draw_game_over/draw_pause don't reference removed features/states.

def draw_main_menu(surface, highscore, assets):
    """Draws the professional Main Menu."""
    assets.draw_background(surface)
    
    # Title with shadow effect
    title_font = assets.font_normal if assets.font_normal else pg.font.SysFont(None, 80)
    shadow_offset = 3
    draw_text(surface, TITLE, 80, SCREEN_WIDTH // 2 + shadow_offset, SCREEN_HEIGHT * 0.2 + shadow_offset, BLACK, title_font, align="center")
    draw_text(surface, TITLE, 80, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.2, ACCENT, title_font, align="center")

    # High Score with improved styling
    score_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 40)
    draw_text(surface, f"High Score: {highscore}", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.35, WHITE, score_font, align="center")

    # Menu options with improved styling and spacing
    menu_y_start = SCREEN_HEIGHT * 0.5  # Moved down from 0.6
    line_height = 80  # Increased from 60
    option_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 36)
    
    # Create semi-transparent backgrounds for menu options
    option_bg = pg.Surface((300, 45), pg.SRCALPHA)
    option_bg.fill((0, 0, 0, 128))
    
    # Start Game
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - 150, menu_y_start - 22))
    draw_text(surface, "START GAME", 36, SCREEN_WIDTH // 2, menu_y_start, WHITE, option_font, align="center")
    draw_text(surface, "[ ENTER ]", 24, SCREEN_WIDTH // 2, menu_y_start + 25, GRAY, assets.font_tiny, align="center")
    
    # Fullscreen Toggle
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - 150, menu_y_start + line_height - 22))
    draw_text(surface, "TOGGLE FULLSCREEN", 36, SCREEN_WIDTH // 2, menu_y_start + line_height, WHITE, option_font, align="center")
    draw_text(surface, f"[ {pg.key.name(FULLSCREEN_TOGGLE_KEY).upper()} ]", 24, SCREEN_WIDTH // 2, menu_y_start + line_height + 25, GRAY, assets.font_tiny, align="center")
    
    # Quit
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - 150, menu_y_start + line_height * 2 - 22))
    draw_text(surface, "QUIT GAME", 36, SCREEN_WIDTH // 2, menu_y_start + line_height * 2, WHITE, option_font, align="center")
    draw_text(surface, "[ Q ]", 24, SCREEN_WIDTH // 2, menu_y_start + line_height * 2 + 25, GRAY, assets.font_tiny, align="center")

    # Controls with improved styling
    controls_bg = pg.Surface((600, 40), pg.SRCALPHA)
    controls_bg.fill((0, 0, 0, 128))
    surface.blit(controls_bg, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 50))
    controls_text = "CONTROLS: LEFT/RIGHT = Move | UP/SPACE = Jump | P = Pause"
    draw_text(surface, controls_text, 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, LIGHT_GRAY, assets.font_tiny, align="center")

def draw_game_over(surface, score, highscore, new_highscore, assets):
    """Draws the professional Game Over screen."""
    assets.draw_background(surface)
    overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0,0))

    title_font = assets.font_normal if assets.font_normal else pg.font.SysFont(None, 80)
    score_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 50)
    info_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 36)

    # Game Over Text with shadow
    shadow_offset = 3
    draw_text(surface, "GAME OVER", 80, SCREEN_WIDTH // 2 + shadow_offset, SCREEN_HEIGHT * 0.25 + shadow_offset, BLACK, title_font, align="center")
    draw_text(surface, "GAME OVER", 80, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.25, RED, title_font, align="center")

    # Score Display with improved styling
    y_start = SCREEN_HEIGHT * 0.45
    if new_highscore:
        new_hs_bg = pg.Surface((300, 45), pg.SRCALPHA)
        new_hs_bg.fill((0, 0, 0, 128))
        surface.blit(new_hs_bg, (SCREEN_WIDTH // 2 - 150, y_start - 45))
        draw_text(surface, "NEW HIGH SCORE!", 36, SCREEN_WIDTH // 2, y_start - 22, GOLD, info_font, align="center")
    
    score_bg = pg.Surface((300, 60), pg.SRCALPHA)
    score_bg.fill((0, 0, 0, 128))
    surface.blit(score_bg, (SCREEN_WIDTH // 2 - 150, y_start))
    draw_text(surface, f"SCORE: {score}", 50, SCREEN_WIDTH // 2, y_start + 30, WHITE, score_font, align="center")
    
    best_bg = pg.Surface((300, 45), pg.SRCALPHA)
    best_bg.fill((0, 0, 0, 128))
    surface.blit(best_bg, (SCREEN_WIDTH // 2 - 150, y_start + 70))
    draw_text(surface, f"BEST: {highscore}", 36, SCREEN_WIDTH // 2, y_start + 92, ACCENT, info_font, align="center")

    # Options with improved styling
    option_y = SCREEN_HEIGHT * 0.75
    option_spacing = 200
    option_bg = pg.Surface((150, 45), pg.SRCALPHA)
    option_bg.fill((0, 0, 0, 128))
    
    # Replay
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - option_spacing - 75, option_y - 22))
    draw_text(surface, "REPLAY", 36, SCREEN_WIDTH // 2 - option_spacing, option_y, WHITE, info_font, align="center")
    draw_text(surface, "[ R ]", 24, SCREEN_WIDTH // 2 - option_spacing, option_y + 25, GRAY, assets.font_tiny, align="center")
    
    # Menu
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - 75, option_y - 22))
    draw_text(surface, "MENU", 36, SCREEN_WIDTH // 2, option_y, WHITE, info_font, align="center")
    draw_text(surface, "[ M ]", 24, SCREEN_WIDTH // 2, option_y + 25, GRAY, assets.font_tiny, align="center")
    
    # Quit
    surface.blit(option_bg, (SCREEN_WIDTH // 2 + option_spacing - 75, option_y - 22))
    draw_text(surface, "QUIT", 36, SCREEN_WIDTH // 2 + option_spacing, option_y, WHITE, info_font, align="center")
    draw_text(surface, "[ Q ]", 24, SCREEN_WIDTH // 2 + option_spacing, option_y + 25, GRAY, assets.font_tiny, align="center")

def draw_pause_screen(surface, assets):
    """Draws the professional Pause screen."""
    overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    surface.blit(overlay, (0,0))

    title_font = assets.font_normal if assets.font_normal else pg.font.SysFont(None, 70)
    info_font = assets.font_small if assets.font_small else pg.font.SysFont(None, 36)

    # Paused Text with shadow
    shadow_offset = 3
    draw_text(surface, "PAUSED", 70, SCREEN_WIDTH // 2 + shadow_offset, SCREEN_HEIGHT * 0.3 + shadow_offset, BLACK, title_font, align="center")
    draw_text(surface, "PAUSED", 70, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.3, ACCENT, title_font, align="center")

    # Options with improved styling
    option_y = SCREEN_HEIGHT * 0.55
    line_height = 60
    option_bg = pg.Surface((300, 45), pg.SRCALPHA)
    option_bg.fill((0, 0, 0, 128))
    
    # Resume
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - 150, option_y - 22))
    draw_text(surface, "RESUME", 36, SCREEN_WIDTH // 2, option_y, WHITE, info_font, align="center")
    draw_text(surface, "[ P ]", 24, SCREEN_WIDTH // 2, option_y + 25, GRAY, assets.font_tiny, align="center")
    
    # Main Menu
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - 150, option_y + line_height - 22))
    draw_text(surface, "MAIN MENU", 36, SCREEN_WIDTH // 2, option_y + line_height, WHITE, info_font, align="center")
    draw_text(surface, "[ M ]", 24, SCREEN_WIDTH // 2, option_y + line_height + 25, GRAY, assets.font_tiny, align="center")
    
    # Quit
    surface.blit(option_bg, (SCREEN_WIDTH // 2 - 150, option_y + line_height * 2 - 22))
    draw_text(surface, "QUIT GAME", 36, SCREEN_WIDTH // 2, option_y + line_height * 2, WHITE, info_font, align="center")
    draw_text(surface, "[ Q ]", 24, SCREEN_WIDTH // 2, option_y + line_height * 2 + 25, GRAY, assets.font_tiny, align="center")

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