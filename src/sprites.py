"""Sprites for Traffic Evader"""

from typing import Literal
import pygame
from config import WIDTH, HEIGHT, LANE_SWITCH_SPEED


class Player(pygame.sprite.Sprite):
    """Class managing the player"""
    def __init__(self, coords: tuple[int, int]) -> None:
        super().__init__()

        self._raw_image = pygame.image.load("./sprites/blue_car.png").convert_alpha()
        self.image = pygame.transform.scale_by(self._raw_image, 1.2)
        self.rect = self.image.get_rect()

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.current_lane = 2
        self.switching_lane: Literal["left", "right", False] = False
        self.switch_frames = round(15 / LANE_SWITCH_SPEED)
        self.lane_delta_x = round(115 / self.switch_frames)
        self.moving_to = 0

    def move_left(self) -> None:
        if not self.switching_lane and self.current_lane - 1 >= 1:
            self.switching_lane = "left"
            self.current_lane -= 1
            self.moving_to = self.rect.centerx - 115


    def move_right(self) -> None:
        if not self.switching_lane and self.current_lane + 1 <= 4:
            self.switching_lane = "right"
            self.current_lane += 1
            self.moving_to = self.rect.centerx + 115

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

    def draw(self, dest_surface: pygame.Surface):
        """Draw this sprite onto dest_surface."""
        return dest_surface.blit(self.image, self.rect)


class Background(pygame.sprite.Sprite):
    """Class managing game background"""
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.image.load("./sprites/road_4.png")
        self.rect = self.image.get_rect()

        self.rect.x = (WIDTH - self.rect.width) // 2
        self.rect.bottom = HEIGHT

    def update(self):
        """Move background for new frame"""

        # The background is twice the screen size.
        # If half has been shown, reset position back to make it loop infinitely.
        if self.rect.y >= HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.y += 1

    def draw(self, dest_surface: pygame.Surface):
        """Draw this sprite onto dest_surface."""
        second_bg = self.rect.copy()
        second_bg.y -= second_bg.height

        dest_surface.blit(self.image, self.rect)
        dest_surface.blit(self.image, second_bg)
