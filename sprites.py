# sprites.py

import pygame as pg
import random
import math
# --- Use non-relative import for flat structure ---
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, assets):
        super().__init__()
        self.assets = assets
        self.image = pg.Surface((PLAYER_BASE, PLAYER_HEIGHT), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self._draw_player_shape(BLUE)
        self.original_image = self.image.copy()
        self.rect.midbottom = (PLAYER_START_POS[0], PLAYER_GROUND_Y)
        self.pos = vec(self.rect.centerx, self.rect.centery)
        self.vel = vec(0, 0) # Only vertical velocity matters now for jump
        self.is_jumping = False
        self.on_ground = True
        self.flash_timer = 0.0
        self.flash_color = WHITE
        self.is_flashing = False

    def _draw_player_shape(self, color):
        """Draws the player triangle onto self.image."""
        self.image.fill((0,0,0,0)) # Clear with transparency
        points = [
            (self.rect.width // 2, 0),
            (0, self.rect.height),
            (self.rect.width, self.rect.height)
        ]
        outline_color = BLACK # Or choose another contrast color like YELLOW
        line_thickness = 2     # How thick the outline is

        # Draw the main filled polygon
        pg.draw.polygon(self.image, color, points)
        # Draw the outline polygon (last argument is line width)
        pg.draw.polygon(self.image, outline_color, points, line_thickness)

    def jump(self):
        if self.on_ground:
            self.vel.y = PLAYER_JUMP_POWER
            self.is_jumping = True
            self.on_ground = False

    # --- Removed apply_powerup method ---
    # def apply_powerup(self, type):
    #     self.active_powerup_type = type
    #     # self.assets.play_sound("powerup") # REMOVED CALL
    #     if type == 'shield': ... # Removed powerup logic

    def flash(self, color, duration):
        self.flash_color = color
        self.flash_timer = duration
        self.is_flashing = True

    def update(self, dt, **kwargs): # Keep **kwargs
        # Simplified Horizontal Movement
        self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]: self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT]: self.vel.x = PLAYER_SPEED
        self.pos.x += self.vel.x * dt * FPS

        # Vertical Movement (Jump/Gravity)
        self.vel.y += PLAYER_GRAVITY * dt * FPS
        self.pos.y += self.vel.y * dt * FPS

        # Boundaries
        half_width = self.rect.width / 2
        if self.pos.x - half_width < 0: self.pos.x = half_width
        if self.pos.x + half_width > SCREEN_WIDTH: self.pos.x = SCREEN_WIDTH - half_width

        # Ground Check
        self.rect.centerx = round(self.pos.x)
        self.rect.bottom = round(self.pos.y + self.rect.height / 2)
        if self.rect.bottom >= PLAYER_GROUND_Y:
            self.rect.bottom = PLAYER_GROUND_Y
            self.pos.y = self.rect.centery
            self.vel.y = 0
            self.is_jumping = False
            self.on_ground = True
        else:
            self.on_ground = False
        self.rect.center = round(self.pos.x), round(self.pos.y) # Final rect update

        # Ceiling check
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
            self.vel.y = max(0, self.vel.y)

        # Flashing effect update
        current_image = self.original_image.copy()
        if self.is_flashing:
            self.flash_timer -= dt
            if self.flash_timer > 0:
                flash_surf = pg.Surface(self.original_image.get_size()).convert_alpha()
                flash_surf.fill(self.flash_color + (100,))
                current_image.blit(flash_surf, (0,0), special_flags=pg.BLEND_RGBA_ADD)
            else:
                self.is_flashing = False; self.flash_timer = 0
        self.image = current_image


class Item(pg.sprite.Sprite):
    def __init__(self, x, item_type, assets):
        super().__init__()
        self.assets = assets
        self.type = item_type
        self.pulse_offset = random.uniform(0, math.pi * 2)
        self.base_size = 0
        self.original_image = None
        self.image = None

        if self.type == 'collectible':
            self.base_size = ITEM_SIZE_COLLECTIBLE
            self.image = pg.Surface((self.base_size, self.base_size), pg.SRCALPHA)
            pg.draw.circle(self.image, GREEN, (self.base_size // 2, self.base_size // 2), self.base_size // 2)
            self.original_image = self.image.copy()
        elif self.type == 'obstacle':
            self.base_size = ITEM_SIZE_OBSTACLE
            self.image = pg.Surface((self.base_size, self.base_size), pg.SRCALPHA)
            pg.draw.rect(self.image, RED, self.image.get_rect(), border_radius=3)
        else: self.kill()

        if self.image:
            self.rect = self.image.get_rect(center=(x, -self.base_size // 2))
            self.pos = vec(self.rect.center)
            self.vel = vec(0, 0)
        else: self.kill()

    def update(self, dt, current_speed): # Simplified signature
        self.vel.y = current_speed
        self.pos.y += self.vel.y * dt * FPS
        self.rect.centery = round(self.pos.y)

        # Animate collectibles
        if self.type == 'collectible' and self.original_image:
            scale_factor = 1.0 + math.sin(pg.time.get_ticks() * 0.001 * COLLECTIBLE_PULSE_SPEED + self.pulse_offset) * COLLECTIBLE_PULSE_AMOUNT
            new_size = max(1, int(self.base_size * scale_factor))
            if abs(scale_factor - 1.0) > 0.01 and new_size != self.rect.width:
                try:
                    center = self.rect.center
                    scaled_image = pg.transform.scale(self.original_image, (new_size, new_size))
                    self.image = scaled_image
                    self.rect = self.image.get_rect(center=center)
                except (pg.error, ValueError): pass

        if self.rect.top > SCREEN_HEIGHT + 50: self.kill()

# --- PowerUp Class REMOVED ---

class Particle(pg.sprite.Sprite):
    def __init__(self, pos, vel, size, color, lifetime):
        super().__init__()
        self.pos = vec(pos)
        self.vel = vec(vel)
        self.size = max(1, int(size))
        self.color = color
        self.lifetime = max(0.01, lifetime)
        self.life_timer = 0.0
        self.image = pg.Surface((self.size, self.size), pg.SRCALPHA)
        try: pg.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), self.size // 2)
        except ValueError: self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt, **kwargs): # Keep **kwargs
        self.pos += self.vel * dt * FPS
        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.life_timer += dt
        if self.life_timer >= self.lifetime:
            self.kill(); return
        if self.lifetime > 0:
            try:
                alpha = max(0, 255 * (1 - (self.life_timer / self.lifetime)))
                self.image.set_alpha(int(alpha))
            except pg.error: self.kill()
        else: self.kill()