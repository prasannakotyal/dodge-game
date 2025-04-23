# game.py

import pygame as pg
import random
import math
# --- Use non-relative imports for flat structure ---
from settings import *
from sprites import Player, Item, Particle # Removed PowerUp
from ui import (add_score_popup, draw_hud, draw_pause_screen,
                update_and_draw_popups, clear_popups)
vec = pg.math.Vector2

class Game:
    def __init__(self, screen, clock, assets, persistence):
        self.screen = screen
        self.clock = clock
        self.assets = assets
        self.persistence = persistence
        self.player_group = pg.sprite.GroupSingle()
        self.items_group = pg.sprite.Group()
        self.particles_group = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.player = None
        self.score = 0
        self.item_speed = BLOCK_SPEED_START
        self.item_spawn_rate = ITEM_SPAWN_BASE_RATE
        self.collectible_probability = COLLECTIBLE_PROBABILITY_BASE
        self.last_item_spawn_time = 0
        self.paused = False
        self.game_over = False
        self.shake_timer = 0.0
        self.shake_intensity = SCREEN_SHAKE_INTENSITY
        self.shake_offset = vec(0, 0)
        self.game_stats = { "score": 0, "game_near_misses": 0 }

    def _spawn_item(self):
        x_pos = random.randint(ITEM_SIZE_OBSTACLE // 2, SCREEN_WIDTH - ITEM_SIZE_OBSTACLE // 2)
        itype = 'collectible' if random.random() < self.collectible_probability else 'obstacle'
        item = Item(x_pos, itype, self.assets)
        self.all_sprites.add(item)
        self.items_group.add(item)

    def _start_shake(self, duration=SCREEN_SHAKE_DURATION, intensity=SCREEN_SHAKE_INTENSITY):
        self.shake_timer = duration
        self.shake_intensity = intensity

    def _update_shake(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            if self.shake_timer <= 0: self.shake_offset = vec(0, 0)
            else:
                intensity = int(self.shake_intensity)
                self.shake_offset.x = random.randint(-intensity, intensity)
                self.shake_offset.y = random.randint(-intensity, intensity)
        else: self.shake_offset = vec(0, 0)

    def _spawn_particles(self, pos, count, color):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            vel = vec(math.cos(angle), math.sin(angle)) * speed
            size = random.uniform(2, 5)
            lifetime = random.uniform(0.3, 0.7)
            p = Particle(pos, vel, size, color, lifetime)
            self.all_sprites.add(p)
            self.particles_group.add(p)

    def reset(self):
        self.all_sprites.empty()
        self.player_group.empty()
        self.items_group.empty()
        self.particles_group.empty()
        clear_popups()
        self.player = Player(self.assets)
        self.all_sprites.add(self.player)
        self.player_group.add(self.player)
        self.score = 0
        self.item_speed = BLOCK_SPEED_START
        self.last_item_spawn_time = pg.time.get_ticks()
        self.paused = False
        self.game_over = False
        self.shake_timer = 0.0
        self.shake_offset = vec(0, 0)
        self.game_stats = { key: 0 for key in self.game_stats }
        self.assets.update_background(BG_COLOR_DARK_START, BG_COLOR_LIGHT_START) # Reset BG

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            if dt > 0.1: dt = 0.1

            # Event Handling
            for event in pg.event.get():
                if event.type == pg.QUIT: return "quit", self.score
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_p: self.paused = not self.paused
                    if not self.paused:
                        if (event.key == pg.K_UP or event.key == pg.K_SPACE) and self.player: self.player.jump()
                    else: # Pause keys
                         if event.key == pg.K_m: return "menu", self.score
                         if event.key == pg.K_q: return "quit", self.score

            if self.paused:
                # Draw Pause Screen
                self.assets.draw_background(self.screen)
                for sprite in self.all_sprites: self.screen.blit(sprite.image, sprite.rect.topleft)
                current_high_score = self.persistence.get_highscore()
                draw_hud(self.screen, self.score, current_high_score, 0, None, self.assets)
                draw_pause_screen(self.screen, self.assets)
                pg.display.flip()
                continue

            # Updates
            self.item_speed = min(MAX_ITEM_SPEED, BLOCK_SPEED_START + self.score * SPEED_INCREMENT_PER_SCORE)
            self.player_group.update(dt)
            for item in self.items_group: item.update(dt, self.item_speed)
            self.particles_group.update(dt)
            self._update_shake(dt)

            # Spawn items
            now = pg.time.get_ticks()
            spawn_interval_ms = (1000.0 / FPS) * self.item_spawn_rate
            if now - self.last_item_spawn_time > spawn_interval_ms:
                 self._spawn_item()
                 self.last_item_spawn_time = now

            # Collisions
            if self.player:
                collided_items_dict = pg.sprite.groupcollide(self.player_group, self.items_group, False, True, pg.sprite.collide_rect)
                for player_collision_instance, items_hit in collided_items_dict.items():
                    for item in items_hit:
                        if item.type == 'obstacle':
                            self.assets.play_sound("hit")
                            self._start_shake(0.3, 8)
                            player_collision_instance.flash(RED, PLAYER_HIT_FLASH_DURATION)
                            self.game_over = True
                            running = False
                            self.persistence.increment_stat("games_played")
                            self.persistence.increment_stat("total_score", self.score)
                            self.game_stats["score"] = self.score
                            self.persistence.save_data()
                            break
                        elif item.type == 'collectible':
                            score_increase = 1
                            crossed_milestone = ( (self.score + score_increase) // SCORE_MILESTONE > self.score // SCORE_MILESTONE )
                            self.score += score_increase
                            self.persistence.increment_stat("total_collectibles")
                            self.assets.play_sound("collect")
                            add_score_popup(item.rect.center, f"+{score_increase}", YELLOW, self.assets)
                            self._spawn_particles(item.rect.center, 5, GREEN)
                            if crossed_milestone and self.score > 0: self._start_shake(0.1, 3)
                    if not running: break
                # Removed powerup collisions
                # Removed near miss

            if not running: continue
            self.draw()

        final_state = "gameover" if self.game_over else "menu"
        return final_state, self.score

    def draw(self):
        temp_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.assets.draw_background(temp_surface)
        self.all_sprites.draw(temp_surface)
        current_high_score = self.persistence.get_highscore()
        draw_hud(temp_surface, self.score, current_high_score, 0, None, self.assets)
        update_and_draw_popups(temp_surface, self.clock.get_time()/1000.0)
        self.screen.blit(temp_surface, self.shake_offset)
        pg.display.flip()