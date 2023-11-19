"""Game view"""

from random import randint
from typing import Literal
import pygame
from src.views.view import View
from src.sprites import Player, Background, Coin, Obstacle, Explosion
from src.managers import FontManager
from src.config import WIDTH, HEIGHT, INITIAL_SPEED, LEVELS

import src.views.gameover as gameover

class Game(View):
    """Main game view class"""
    def __init__(self, state: dict) -> None:
        super().__init__(state)
        pygame.display.set_caption("Traffic Evader")

        self.fonts = FontManager()
        self.level = LEVELS[self.state["difficulty"]]
        self.player = Player(f"./src/sprites/cars/{self.state['car']}.png", self.level)
        self.background = Background(self.level)
        self.coins: pygame.sprite.Group[Coin] = pygame.sprite.Group()
        self.obstacles: pygame.sprite.Group[Obstacle] = pygame.sprite.Group()
        self.score_text = self.fonts.font_score.render("0", True, "black")

        self.frame_count = 0
        self.speed = INITIAL_SPEED
        self.score = 0

        self.explosion = Explosion()
        self.exploding = False

    def road_position_free(self, lane: int, new_rect: pygame.Rect):
        """Check if a position on the road,
        specified by lane and the rectangle of the object about to be spawned,
        isn't occupied by any other objects.
        This is to avoid layered objects on top of each other.
        Returns true if free, false otherwise."""

        obstacles_on_same_lane = [o.rect for o in self.obstacles if o.lane == lane]
        coins_on_same_lane = [c.rect for c in self.coins if c.lane == lane]

        if new_rect.collidelist(obstacles_on_same_lane) != -1 or new_rect.collidelist(coins_on_same_lane) != -1:
            return False

        return True

    def spawn_road_objects(self, obj: Literal["obstacle", "coin"], amount: int) -> None:
        """Spawn multiple road objects (obstacles or coins)"""
        lane_width = self.level["lane_width"]
        distance_to_road = self.background.rect.left
        obstacle_width = 64
        coin_width = 32

        for _ in range(amount):
            lane = randint(1, self.level["lanes"]) # type: ignore
            height = randint(50, 400)

            # x coordinate:
            # Distance to start of road + 30px side line + x_lanes*lane_width - (1/2)*(lane_width - 10px) - 10px (white line) - 1/2 object width
            pos_x = distance_to_road + 30 + lane*lane_width - (lane_width-10)//2 - 10 # type: ignore

            if obj == "obstacle":
                pos_x -= obstacle_width//2
                new_rect = pygame.rect.Rect((pos_x, -height, 64, 64))

                # If the position on the road isn't free, re-randomize the height
                while not self.road_position_free(lane, new_rect):
                    height = randint(50, 400)
                    new_rect.y = -height

                self.obstacles.add(
                    Obstacle("./src/sprites/obstacles/toyota-prius-front.png", (pos_x, -height), lane)
                )
            elif obj == "coin":
                pos_x -= coin_width//2

                new_rect = pygame.rect.Rect((pos_x, -height, 32, 32))

                while not self.road_position_free(lane, new_rect):
                    height = randint(50, 400)
                    new_rect.y = -height

                self.coins.add(Coin((pos_x, -height), lane))

    def process_input(self) -> None:
        """Process game inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self) -> None:
        """Update: Move sprites, change state variables, etc"""
        if self.exploding:
            self.explosion.update()
            if self.explosion.animation_finished:
                self.active = False
            return

        self.background.update(self.speed)
        self.coins.update(self.speed)
        self.obstacles.update(self.speed)
        self.player.update()

        if len(self.coins) < self.speed:
            diff = self.speed - len(self.coins)
            self.spawn_road_objects("coin", diff)

        if len(self.obstacles) < self.speed // 2:
            diff = self.speed // 2 - len(self.obstacles)
            self.spawn_road_objects("obstacle", diff)

        for coin in self.coins:
            if coin.rect.top > HEIGHT:
                self.coins.remove(coin)

        for obstacle in self.obstacles:
            if obstacle.rect.top > HEIGHT:
                self.obstacles.remove(obstacle)

        collided = pygame.sprite.spritecollideany(self.player, self.obstacles, pygame.sprite.collide_mask)

        if collided:
            self.exploding = True
            overlap_pos = list(
                self.player.mask.overlap(
                    collided.mask,
                    (collided.rect.x - self.player.rect.x, collided.rect.y - self.player.rect.y)
                )
            )
            # Collisions which are (nearly) head-on, should have it's explosion center at midtop of car
            # Needs to be checked, because otherwise overlap()'s first point is used
            # (usually top left, as the function checks for collisions iterably in the mask)
            if overlap_pos[1] < 10:
                self.explosion.rect.center = self.player.rect.midtop
            else:
                overlap_pos[0] += self.player.rect.x
                overlap_pos[1] += self.player.rect.y
                self.explosion.rect.centerx = overlap_pos[0]
                self.explosion.rect.centery = overlap_pos[1]
            self.transition_to = gameover.GameOver(self.state)

        # Third argument specifies to remove any coins collected from the coin sprite group
        coins_collected = pygame.sprite.spritecollide(self.player, self.coins, True, pygame.sprite.collide_mask)
        self.score += len(coins_collected)

        self.score_text = self.fonts.font_score.render(str(self.score), True, "black")

        self.frame_count += 1
        # Each "speed level" duration is constantly increasing
        # (speed is 2 for 1200 frames, speed is 5 for 6000 frames, etc)
        if self.frame_count >= self.speed * 600:
            self.frame_count = 0
            self.speed += 1

    def render(self) -> None:
        """Render: Fill background, blit sprites, etc"""
        self.screen.fill((255, 255, 255))

        self.background.draw(self.screen)
        self.coins.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(self.score_text, (WIDTH - 100, 25))

        if self.exploding:
            self.explosion.draw(self.screen)

        pygame.display.flip()
