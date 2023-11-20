"""Sprites for Traffic Evader"""

from random import randint, choice
from typing import Literal
import pygame
from src.config import WIDTH, HEIGHT, LANE_SWITCH_SPEED, CARS_OBSTACLES

class GameObject(pygame.sprite.Sprite):
    def __init__(self, img_path: str, scale: float | tuple[int, int] | None = None) -> None:
        super().__init__()

        self.image = pygame.image.load(img_path).convert_alpha()

        if scale and isinstance(scale, float):
            self.image = pygame.transform.scale_by(self.image, scale)
        elif scale and isinstance(scale, tuple):
            self.image = pygame.transform.scale(self.image, scale)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, dest_surface: pygame.Surface):
        """Draw this sprite onto dest_surface."""
        return dest_surface.blit(self.image, self.rect)

class Player(GameObject):
    """Class managing the player"""
    def __init__(self, img_path: str, level: dict) -> None:
        super().__init__(img_path, (75, 75))

        self.level_info = level

        self.rect.x = self.level_info["player"]["init_x"]
        self.rect.y = 400

        self.current_lane = self.level_info["player"]["init_lane"]
        self.switching_lane: Literal["left", "right", False] = False
        self.switch_frames = round(15 / LANE_SWITCH_SPEED)
        self.lane_delta_x = round(self.level_info["lane_width"] / self.switch_frames)
        self.moving_to = 0

    def move_left(self) -> None:
        if not self.switching_lane and self.current_lane - 1 >= 1:
            self.switching_lane = "left"
            self.current_lane -= 1
            self.moving_to = self.rect.centerx - self.level_info["lane_width"]


    def move_right(self) -> None:
        if not self.switching_lane and self.current_lane + 1 <= self.level_info["lanes"]:
            self.switching_lane = "right"
            self.current_lane += 1
            self.moving_to = self.rect.centerx + self.level_info["lane_width"]

    def update(self) -> None:
        if self.switching_lane == "left":
            # Only move player by delta_x if it won't move it too far (inaccuracy caused by rounding)
            if self.rect.centerx - self.lane_delta_x > self.moving_to:
                self.rect.centerx -= self.lane_delta_x
            else:
                self.rect.centerx = self.moving_to
                self.switching_lane = False

        if self.switching_lane == "right":
            # Only move player by delta_x if it won't move it too far (inaccuracy caused by rounding)
            if self.rect.centerx + self.lane_delta_x < self.moving_to:
                self.rect.centerx += self.lane_delta_x
            else:
                self.rect.centerx = self.moving_to
                self.switching_lane = False

class Coin(GameObject):
    def __init__(self, position: tuple[int, int], lane: int) -> None:
        super().__init__("./src/sprites/coin.png", (160, 32))

        # self.image and self.rect will be overwritten with coin used from the sprite sheet
        self.sheet_img = self.image
        self.sheet_rect = self.rect

        self.frame_counter = 0
        self.current_sprite = 0
        self.sprites = 4

        # Create a 32x32 surface and blit initial sprite onto it
        self.image = pygame.surface.Surface((32, 32), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(self.sheet_img, (0, 0), self.rect)

        # Overwrite mask to use correct surface instead of whole spritesheet
        self.mask = pygame.mask.from_surface(self.image)

        self.lane = lane
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self, speed: int):
        self.frame_counter += 1

        if self.frame_counter >= 8:
            if self.current_sprite + 1 >= self.sprites:
                self.current_sprite = 0
            else:
                self.current_sprite += 1

            self.image.fill((0, 0, 0, 0))
            # Move the area (third argument) based on the next coin sprite to be shown
            self.image.blit(self.sheet_img, (0, 0), (self.current_sprite*32, 0, 32, 32))

            self.frame_counter = 0

        self.rect.y += speed

class Obstacle(GameObject):
    def __init__(self, position: tuple[int, int], lane: int):
        self.img_path = self.select_random_car()
        super().__init__(self.img_path, (64, 64))

        self.rect.x = position[0]
        self.rect.y = position[1]
        self.lane = lane

    def select_random_car(self) -> str:
        rand = randint(1, 100)
        obstacles_path = "./src/sprites/obstacles/"

        if rand <= 60:
            return obstacles_path + choice(CARS_OBSTACLES["low"])
        if rand <= 97:
            return obstacles_path + choice(CARS_OBSTACLES["medium"])

        return obstacles_path + choice(CARS_OBSTACLES["high"])

    def update(self, speed: int):
        """Move obstacle for new frame"""
        self.rect.y += speed

class Explosion(GameObject):
    def __init__(self) -> None:
        super().__init__("./src/sprites/explosion.png", (640, 80))

        self.sheet_img = self.image
        self.sheet_rect = self.rect

        self.image = pygame.surface.Surface((80, 80), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(self.sheet_img, (0, 0), self.rect)

        self.frame_counter = 0
        self.sprite_frames = self.sheet_rect.width // self.rect.width
        self.current_sprite = 1
        self.animation_finished = False

    def update(self) -> None:
        """Updates explosion sprite"""
        self.frame_counter += 1
        if self.frame_counter >= 12:
            self.frame_counter = 0
            self.current_sprite += 1

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sheet_img, (0, 0), (self.current_sprite*80, 0, 80, 80))

        if self.current_sprite >= self.sprite_frames:
            self.animation_finished = True

class Background(GameObject):
    """Class managing game background"""
    def __init__(self, level: dict) -> None:
        super().__init__(f"./src/sprites/road_{level['lanes']}.png")

        self.level_info = level
        self.rect.x = (WIDTH - self.rect.width) // 2
        self.rect.bottom = HEIGHT

    def update(self, speed: int):
        """Move background for new frame"""

        # The background is twice the screen size.
        # If half has been shown, reset position back to make it loop infinitely.
        if self.rect.y >= HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.y += speed

    def draw(self, dest_surface: pygame.Surface):
        second_bg = self.rect.copy()
        second_bg.y -= second_bg.height

        dest_surface.blit(self.image, self.rect)
        dest_surface.blit(self.image, second_bg)
