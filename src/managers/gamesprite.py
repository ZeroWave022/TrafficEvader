"""Game sprite manager"""

from typing import Literal
from random import randint
import pygame
from src.config import HEIGHT, LEVELS
from src.sprites import Player, Background, Coin, Obstacle, Explosion
from src.utils import asset_path

class GameSpriteManager:
    """Class managing spawning, despawning and updating sprites.
    Used by the Game view."""
    def __init__(self, state: dict) -> None:
        self.level = LEVELS[state["difficulty"]]

        car_name = state["car"]
        self.player = Player(asset_path(f"sprites/cars/{car_name}"), self.level)
        self.background = Background(self.level)
        self.coins: pygame.sprite.Group[Coin] = pygame.sprite.Group()
        self.obstacles: pygame.sprite.Group[Obstacle] = pygame.sprite.Group()

        # Special sprite which is rendered manually and managed by the Game view
        self.explosion = Explosion()

    def update(self, speed: int):
        self.background.update(speed)
        self.coins.update(speed)
        self.obstacles.update(speed)
        self.player.update()

    def spawn_road_objects(self, speed: int):
        if len(self.coins) < speed:
            diff = speed - len(self.coins)
            if diff < 3:
                self._add_road_objects("coin", diff, speed)
            else:
                self._add_road_objects("coin", 3, speed)

        if len(self.obstacles) < speed // 2:
            diff = speed // 2 - len(self.obstacles)
            if diff < 3:
                self._add_road_objects("obstacle", diff, speed)
            else:
                self._add_road_objects("obstacle", 3, speed)

    def despawn_obsolete(self) -> None:
        for coin in self.coins:
            if coin.rect.top > HEIGHT:
                self.coins.remove(coin)

        for obstacle in self.obstacles:
            if obstacle.rect.top > HEIGHT:
                self.obstacles.remove(obstacle)

    def spawn_explosion(self, collided_with: Obstacle) -> None:
        overlap_pos = list(
            self.player.mask.overlap(
                collided_with.mask,
                (collided_with.rect.x - self.player.rect.x, collided_with.rect.y - self.player.rect.y)
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

    def _add_road_objects(self, obj: Literal["obstacle", "coin"], amount: int, speed: int) -> None:
        """Adds/spawns multiple road objects (obstacles or coins)"""
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
                    height = randint(50, speed * 100)
                    new_rect.y = -height

                self.obstacles.add(
                    Obstacle((pos_x, -height), lane)
                )
            elif obj == "coin":
                pos_x -= coin_width//2
                new_rect = pygame.rect.Rect((pos_x, -height, 32, 32))

                while not self.road_position_free(lane, new_rect):
                    height = randint(50, speed * 100)
                    new_rect.y = -height

                self.coins.add(Coin((pos_x, -height), lane))

    def draw(self, dest_surface: pygame.Surface) -> None:
        self.background.draw(dest_surface)
        self.coins.draw(dest_surface)
        self.obstacles.draw(dest_surface)
        self.player.draw(dest_surface)
