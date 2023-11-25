"""Game view"""

from typing import Literal
from random import randint
import pygame
from src.views.view import View
from src.sprites import Player, Background, Coin, Obstacle, Explosion
from src.config import HEIGHT, LEVELS, WIDTH, INITIAL_SPEED
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

    def update(self, speed: int) -> None:
        """Update game sprites"""
        self.background.update(speed)
        self.coins.update(speed)
        self.obstacles.update(speed)
        self.player.update()

    def spawn_road_objects(self, speed: int) -> None:
        """Spawn road objects for a new frame, if needed."""
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
        """Despawn road objects which are no longer visible."""
        for coin in self.coins:
            if coin.rect.top > HEIGHT:
                self.coins.remove(coin)

        for obstacle in self.obstacles:
            if obstacle.rect.top > HEIGHT:
                self.obstacles.remove(obstacle)

    def spawn_explosion(self, collided_with: Obstacle) -> None:
        """Spawns an explosion in the point of collision between the player and collided_with.
        Only supposed to be used when the game is over."""
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

    def road_position_free(self, lane: int, new_rect: pygame.Rect) -> bool:
        """Check if a position on the road,
        specified by lane and the rectangle of the object about to be spawned,
        isn't occupied by any other objects.
        This is to avoid layered objects on top of each other.
        Returns a bool indicating if the position is free."""

        obstacles_on_same_lane = [o.rect for o in self.obstacles if o.lane == lane]
        coins_on_same_lane = [c.rect for c in self.coins if c.lane == lane]

        if new_rect.collidelist(obstacles_on_same_lane) != -1 or new_rect.collidelist(coins_on_same_lane) != -1:
            return False

        return True

    def _add_road_objects(self, obj: Literal["obstacle", "coin"], amount: int, speed: int) -> None:
        """Add/spawn multiple road objects (obstacles or coins)"""
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
        """Draw all game sprites onto dest_surface."""
        self.background.draw(dest_surface)
        self.coins.draw(dest_surface)
        self.obstacles.draw(dest_surface)
        self.player.draw(dest_surface)


class Game(View):
    """Main game view class"""
    def __init__(self, state: dict) -> None:
        super().__init__(state)
        pygame.display.set_caption("Traffic Evader")

        self.sprites = GameSpriteManager(self.state)
        
        self.score_text = self.fonts.font_score.render("0", True, "black")

        self.frame_count = 0
        self.speed = INITIAL_SPEED
        self.score = 0

        self.exploding = False

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.sprites.player.move_left()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.sprites.player.move_right()

    def update(self) -> None:
        # Special state: While explosion is happening,
        # (before moving to game over screen), no other updates are executed
        if self.exploding:
            self.sprites.explosion.update()
            if self.sprites.explosion.animation_finished:
                self.active = False
            return

        self.sprites.update(self.speed)
        self.sprites.spawn_road_objects(self.speed)
        self.sprites.despawn_obsolete()

        collided = pygame.sprite.spritecollideany(self.sprites.player, self.sprites.obstacles, pygame.sprite.collide_mask)

        if collided:
            self.exploding = True
            self.sounds.explosion.play()
            self.sprites.spawn_explosion(collided)
            self.transition_to = "gameover"

        # Third argument specifies to remove any coins collected from the coin sprite group
        coins_collected = pygame.sprite.spritecollide(self.sprites.player, self.sprites.coins, True, pygame.sprite.collide_mask)

        self.score += len(coins_collected)
        if len(coins_collected) > 0 and self.score % 10 == 0:
            self.sounds.coin.play()

        self.score_text = self.fonts.font_score.render(str(self.score), True, "black")

        self.frame_count += 1
        # Each "speed level" duration is constantly increasing
        # (speed is 2 for 1200 frames, speed is 5 for 6000 frames, etc)
        if self.frame_count >= self.speed * 600:
            self.frame_count = 0
            self.speed += 1

    def render(self) -> None:
        self.screen.fill((255, 255, 255))

        self.sprites.draw(self.screen)
        self.screen.blit(self.score_text, (WIDTH - 100, 25))

        if self.exploding:
            self.sprites.explosion.draw(self.screen)

        pygame.display.flip()
