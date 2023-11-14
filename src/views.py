"""Traffic Evader views"""

import sys
from random import randint
from typing import Literal
import pygame
from sprites import Player, Background, Coin, Obstacle
from ui import Button, SelectableItem, ItemSelector
from managers import FontManager
from config import WIDTH, HEIGHT, FPS, INITIAL_SPEED, LEVELS

class View():
    """A base class for all game views with a game loop"""
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.active = True
        self.transition_to: View | None = None

    def process_input(self) -> None:
        """Game loop part 1: Process game inputs.
        Override this method when inheriting."""

    def update(self) -> None:
        """Game loop part 2: Move sprites, change state variables, etc.
        Override this method when inheriting."""

    def render(self) -> None:
        """Game loop part 3: Fill background, blit sprites, etc.
        Override this method when inheriting.
        """

    def run(self):
        """Run game loop"""
        while self.active:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def exit(self):
        """Quit pygame and end python process"""
        pygame.quit()
        sys.exit()


class Game(View):
    """Main game view class"""
    def __init__(self, difficulty_name: str) -> None:
        super().__init__()
        pygame.display.set_caption("Traffic Evader")

        self.level = LEVELS[difficulty_name]
        self.player = Player(self.level)
        self.background = Background(self.level)
        self.coins: pygame.sprite.Group[Coin] = pygame.sprite.Group()
        self.obstacles: pygame.sprite.Group[Obstacle] = pygame.sprite.Group()

        self.frame_count = 0
        self.speed = INITIAL_SPEED
        self.fonts = FontManager()

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
                    Obstacle("./sprites/toyota-prius-front.png", (pos_x, -height), lane)
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

        if pygame.sprite.spritecollideany(self.player, self.obstacles, pygame.sprite.collide_mask):
            self.active = False
            self.transition_to = GameOver()

        # Third argument specifies to remove any coins collected from the coin sprite group
        pygame.sprite.spritecollide(self.player, self.coins, True, pygame.sprite.collide_mask)

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

        pygame.display.flip()

class GameOver(View):
    def __init__(self) -> None:
        super().__init__()

        self.fonts = FontManager()
        self.text = self.fonts.font_title.render("Game Over", True, "black", (255, 255, 255))

        self.retry = Button((WIDTH // 2 - 75, HEIGHT // 2 - 120, 150, 50), text="Retry")
        self.back = Button((WIDTH // 2 - 75, HEIGHT // 2 - 60, 150, 50), text="Back to Menu")
        self.exit_btn = Button((WIDTH // 2 - 75, HEIGHT // 2, 150, 50), text="Exit")

        self.buttons = [self.retry, self.back, self.exit_btn]

        self.overlay = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((50, 50, 50, 150))
        self.overlay_blitted = False

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click_event()

        if self.retry.clicked or self.back.clicked:
            self.active = False

        if self.retry.clicked:
            self.transition_to = Game("normal")

        if self.back.clicked:
            self.transition_to = Menu()

        if self.exit_btn.clicked:
            self.exit()

    def render(self) -> None:
        if not self.overlay_blitted:
            self.screen.blit(self.overlay, (0, 0))
            self.overlay_blitted = True

        for button in self.buttons:
            button.draw(self.screen)
        
        self.screen.blit(self.text, ((WIDTH - self.text.get_width()) // 2, HEIGHT - 450))

        pygame.display.flip()

class Menu(View):
    """Main menu view class"""
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Traffic Evader")

        self.fonts = FontManager()
        self.title = self.fonts.font_title.render("Traffic Evader", True, "black")

        self.play = Button((WIDTH // 2 - 75, HEIGHT - 350, 150, 50), text="Play")
        self.settings = Button((WIDTH // 2 - 75, HEIGHT - 290, 150, 50), text="Settings")
        self.exit_btn = Button((WIDTH // 2 - 75, HEIGHT - 230, 150, 50), text="Quit")

        self.buttons = [self.play, self.settings, self.exit_btn]

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click_event()

        if self.play.clicked:
            self.active = False
            self.transition_to = Game("normal")

        if self.settings.clicked:
            self.active = False
            self.transition_to = Settings()

        if self.exit_btn.clicked:
            self.exit()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))

        for button in self.buttons:
            button.draw(self.screen)

        self.screen.blit(self.title, ((WIDTH - self.title.get_width()) // 2, HEIGHT - 450))

        pygame.display.flip()

class Settings(View):
    def __init__(self) -> None:
        super().__init__()

        self.cars = [[
            SelectableItem("./sprites/blue_car.png", (80, 80)),
            SelectableItem("./sprites/blue_car.png", (80, 80)),
            SelectableItem("./sprites/blue_car.png", (80, 80)),
            SelectableItem("./sprites/blue_car.png", (80, 80)),
        ]]

        self.car_selector = ItemSelector(self.cars, (0, 1))

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.car_selector.process_input(mouse_pos)

    def render(self):
        self.screen.fill((255, 255, 255))

        self.car_selector.draw(self.screen)

        pygame.display.flip()
