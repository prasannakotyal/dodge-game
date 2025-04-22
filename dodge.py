# Simple Dodge Game using Pygame with Menu, High-Score Tracking, SINGLE LIFE, and JUMPING
# -------------------------------------------------------------------------------
# Controls:
#   - LEFT/RIGHT arrows to move horizontally
#   - UP Arrow or SPACE to Jump
#   - ENTER to select
#   - R to replay, Q to quit on Game Over screen
# Requirements:
#   - pygame (pip install pygame)
#   - (Optional) Sound files: collect.wav, hit.wav in the same directory

import pygame
import random
import sys
import os
import math # Needed for drawing triangle player

# Configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60
PLAYER_BASE = 50  # Base width of the player triangle
PLAYER_HEIGHT = 40 # Height of the player triangle
PLAYER_SPEED = 7   # Horizontal speed
PLAYER_GROUND_Y_OFFSET = 10 # How far from the bottom the player rests
ITEM_SIZE = 40 # Size for both obstacles and collectibles
BLOCK_SPEED_START = 3.5      # initial fall speed
SPEED_INCREMENT = 0.06       # speed increase per collectible gathered
MAX_ITEM_SPEED = 10          # cap for maximum fall speed
ITEM_SPAWN_RATE = 28         # frames per new item (lower is more frequent)
COLLECTIBLE_PROBABILITY = 0.65 # % chance to spawn a collectible
HIGHSCORE_FILE = "highscore.txt"

# --- Single Life ---
LIVES_START = 1              # number of lives (now always 1)

# --- Jump Mechanics ---
GRAVITY = 0.6               # Acceleration downwards
JUMP_POWER = -13            # Initial upward velocity on jump

# Colors (expanded)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (100, 100, 255) # Player color
YELLOW = (255, 255, 0)
DARK_BG = (20, 20, 40)
LIGHT_BG = (40, 40, 80)
GRAY = (200, 200, 200)
LIGHT_GRAY = (160, 160, 160)

# Initialize Pygame & Mixer
pygame.init()
try:
    pygame.mixer.init()
    collect_sound = pygame.mixer.Sound("collect.wav")
    hit_sound = pygame.mixer.Sound("hit.wav")
    sounds_enabled = True
except (pygame.error, FileNotFoundError) as e: # Catch both errors
    print(f"Warning: Could not initialize sound mixer or load sounds ({e}). Running without sound.")
    sounds_enabled = False
    collect_sound = None
    hit_sound = None


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge and Collect!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 52)
small_font = pygame.font.SysFont(None, 36)
tiny_font = pygame.font.SysFont(None, 24) # For score popups

# --- High-Score Management (Unchanged) ---
def get_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, 'r') as f:
        try:
            content = f.read().strip()
            return int(content) if content else 0
        except ValueError:
            return 0

def set_highscore(score):
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(str(score))

# --- Main Menu (Updated Controls Info) ---
def show_main_menu(highscore):
    screen.fill(DARK_BG) # Use dark background
    title_surf = font.render("Dodge and Collect!", True, YELLOW)
    subtitle_surf = small_font.render("(Get Jiggy)", True, LIGHT_GRAY)
    hs_surf = small_font.render(f"High Score: {highscore}", True, WHITE)
    prompt_surf = small_font.render("Press ENTER to Start", True, GRAY)
    controls_surf_move = tiny_font.render("Controls: LEFT/RIGHT Arrows = Move", True, GRAY)
    controls_surf_jump = tiny_font.render("UP Arrow / SPACE = Jump", True, GRAY)


    screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 140)))
    screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)))
    screen.blit(hs_surf, hs_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
    screen.blit(prompt_surf, prompt_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))
    screen.blit(controls_surf_move, controls_surf_move.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70)))
    screen.blit(controls_surf_jump, controls_surf_jump.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 95)))

    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return
                elif e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

# --- Function to draw the player triangle (Unchanged) ---
def draw_player(surface, rect, color):
    points = [
        (rect.centerx, rect.top),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ]
    pygame.draw.polygon(surface, color, points)

# --- Function to draw background gradient (Unchanged) ---
def draw_background(surface):
    for y in range(SCREEN_HEIGHT):
        color_ratio = y / SCREEN_HEIGHT
        color = (
            int(DARK_BG[0] * (1 - color_ratio) + LIGHT_BG[0] * color_ratio),
            int(DARK_BG[1] * (1 - color_ratio) + LIGHT_BG[1] * color_ratio),
            int(DARK_BG[2] * (1 - color_ratio) + LIGHT_BG[2] * color_ratio)
        )
        surface.fill(color, (0, y, SCREEN_WIDTH, 1))

# --- Score Popup Effect (Unchanged except global frame_count) ---
score_popups = [] # List to store popups: [text_surface, rect, creation_time]
POPUP_DURATION = 0.5 * FPS # Frames a popup should last
frame_count = 0 # Make frame_count global for popup timing

def add_score_popup(position, text="+1"):
    global frame_count # Need to access global frame_count
    text_surf = tiny_font.render(text, True, YELLOW)
    rect = text_surf.get_rect(center=position)
    score_popups.append([text_surf, rect, frame_count])

def update_and_draw_popups(surface):
    global frame_count # Need to access global frame_count
    active_popups = []
    current_frame = frame_count # Use the global frame_count
    for popup in score_popups:
        text_surf, rect, creation_time = popup
        if current_frame - creation_time < POPUP_DURATION:
            rect.y -= 1 # Move popup slightly up
            alpha = max(0, 255 - int(255 * ((current_frame - creation_time) / POPUP_DURATION)))
            text_surf.set_alpha(alpha)
            surface.blit(text_surf, rect)
            active_popups.append(popup)
    score_popups[:] = active_popups

# --- Game Loop (Major Changes for Jump and Single Life) ---
def run_game():
    global frame_count # Use the global frame_count
    player_ground_y = SCREEN_HEIGHT - PLAYER_HEIGHT - PLAYER_GROUND_Y_OFFSET
    player_rect = pygame.Rect(
        (SCREEN_WIDTH - PLAYER_BASE) // 2,
        player_ground_y, # Start at ground level
        PLAYER_BASE,
        PLAYER_HEIGHT
    )
    player_y_velocity = 0
    is_jumping = False

    items = []
    frame_count = 0 # Reset frame count for this game instance
    score = 0
    lives = LIVES_START # Will be 1
    running = True

    while running and lives > 0: # Loop continues only while lives > 0
        dt = clock.tick(FPS) / 1000.0
        frame_count += 1

        # --- Event Handling (Includes Jump Trigger) ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                # Jump input
                if (e.key == pygame.K_UP or e.key == pygame.K_SPACE) and not is_jumping:
                    player_y_velocity = JUMP_POWER
                    is_jumping = True

        # --- Player Horizontal Movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += PLAYER_SPEED

        # --- Player Vertical Movement (Physics) ---
        player_y_velocity += GRAVITY
        player_rect.y += player_y_velocity

        # Check for landing
        if player_rect.bottom >= player_ground_y:
            player_rect.bottom = player_ground_y
            player_y_velocity = 0
            is_jumping = False # Can jump again once landed

        # Prevent going off the top (optional, gravity usually handles this)
        if player_rect.top < 0:
            player_rect.top = 0
            player_y_velocity = max(0, player_y_velocity) # Stop upward motion if hitting ceiling


        # --- Spawn new item periodically ---
        if frame_count % ITEM_SPAWN_RATE == 0:
            x_pos = random.randint(0, SCREEN_WIDTH - ITEM_SIZE)
            item_rect = pygame.Rect(x_pos, -ITEM_SIZE, ITEM_SIZE, ITEM_SIZE)
            if random.random() < COLLECTIBLE_PROBABILITY:
                item_type = 'collectible'
            else:
                item_type = 'obstacle'
            items.append({'rect': item_rect, 'type': item_type})

        # --- Calculate current item speed, capped ---
        item_speed = BLOCK_SPEED_START + score * SPEED_INCREMENT
        item_speed = min(item_speed, MAX_ITEM_SPEED)

        # --- Move items & Check collisions ---
        items_to_keep = []
        collision_occurred = False

        for item in items:
            item['rect'].y += item_speed

            # Check collision with player
            if item['rect'].colliderect(player_rect):
                if item['type'] == 'obstacle':
                    lives -= 1 # This will immediately make lives 0
                    if sounds_enabled and hit_sound: hit_sound.play()
                    collision_occurred = True
                    # Game ends here, no need for reset logic within the loop
                    break # Exit item loop immediately on fatal collision

                elif item['type'] == 'collectible':
                    score += 1
                    if sounds_enabled and collect_sound: collect_sound.play()
                    add_score_popup(item['rect'].center)
                    # Don't add collected item to items_to_keep list
                    continue # Skip boundary check for collected item

            # Check if item is off-screen and add to keep list if it is
            if item['rect'].top <= SCREEN_HEIGHT:
                items_to_keep.append(item)

        items = items_to_keep # Update the list (unless a fatal collision occurred)

        # --- Render ---
        draw_background(screen)
        draw_player(screen, player_rect, BLUE)

        for item in items:
            if item['type'] == 'obstacle':
                pygame.draw.rect(screen, RED, item['rect'])
            elif item['type'] == 'collectible':
                pygame.draw.circle(screen, GREEN, item['rect'].center, ITEM_SIZE // 2)

        update_and_draw_popups(screen)

        # Draw score (top left)
        score_surf = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        # --- REMOVED LIVES DISPLAY ---
        # No need to draw lives when there's only one

        pygame.display.flip()
        # End of main game loop (while running and lives > 0)

    # Return score after the loop ends (due to lives becoming 0 or other reasons)
    score_popups.clear() # Clear any remaining popups before game over
    return score

# --- Game Over Screen (Unchanged Functionally) ---
def show_game_over(score, highscore):
    screen.fill(BLACK)
    over_surf = font.render("Game Over!", True, RED)
    score_surf = small_font.render(f"Your Score: {score}", True, WHITE)
    hs_surf = small_font.render(f"High Score: {highscore}", True, YELLOW)
    prompt_surf = small_font.render("R = Replay  |  Q = Quit", True, GRAY)

    screen.blit(over_surf, over_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)))
    screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
    screen.blit(hs_surf, hs_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10)))
    screen.blit(prompt_surf, prompt_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70)))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True  # Replay
                elif e.key == pygame.K_q:
                    return False # Quit
        clock.tick(FPS)

# --- Entry Point (Updated highscore logic slightly) ---
def main():
    # Initialize highscore once at the start
    highscore = get_highscore()
    while True:
        show_main_menu(highscore) # Show current highscore
        score = run_game()

        # Update highscore *only if* the new score is better
        if score > highscore:
            highscore = score
            set_highscore(score)
        # Always get the latest highscore before showing game over,
        # ensures display is correct even if not beaten.
        # (Though in single-process game, 'highscore' variable should be accurate)
        # current_hs = get_highscore() # Can use this instead of relying on 'highscore' variable state

        # Pass the potentially updated highscore to the game over screen
        if not show_game_over(score, highscore):
            break # Exit if player chooses Quit

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()