"""Background sprite"""

import pygame
from src.config import WIDTH, HEIGHT
from src.utils import asset_path
from .gameobject import GameObject


class Background(GameObject):
    """Class managing game background"""

    def __init__(self, level: dict) -> None:
        lanes_num = level["lanes"]
        # Road is the "main" sprite, so self.image and self.rect refer to the road
        super().__init__(asset_path(f"sprites/road_{lanes_num}.png"))

        # Set road position
        self.rect.x = (WIDTH - self.rect.width) // 2
        self.rect.bottom = HEIGHT

        # Load background and set up left and right side
        raw_bg = pygame.image.load(asset_path("sprites/background.png")).convert_alpha()
        self.bg_left = pygame.transform.rotate(raw_bg, 90)
        self.bg_right = pygame.transform.flip(self.bg_left, True, False)

        self.bg_left_rect = self.bg_left.get_rect()
        self.bg_right_rect = self.bg_right.get_rect()

        self.bg_left_rect.right = self.rect.left
        self.bg_right_rect.x = self.rect.right

        self.bg_left_rect.bottom = HEIGHT
        self.bg_right_rect.bottom = HEIGHT

    def update(self, speed: int) -> None:
        """Move background for new frame"""
        # The road and background are blitted twice.
        # If half has been shown, reset position back to make it loop infinitely.
        if self.rect.y >= HEIGHT:
            self.rect.bottom = HEIGHT

        if self.bg_left_rect.y >= HEIGHT:
            self.bg_left_rect.bottom = HEIGHT
            self.bg_right_rect.bottom = HEIGHT

        self.rect.y += speed
        self.bg_left_rect.y += speed
        self.bg_right_rect.y += speed

    def draw(self, dest_surface: pygame.Surface) -> None:
        # Blit road
        dest_surface.blit(self.image, self.rect)
        dest_surface.blit(self.image, (self.rect.x, self.rect.y - self.rect.height))

        bg_height = self.bg_left_rect.height

        # Blit left background
        dest_surface.blit(self.bg_left, self.bg_left_rect)
        dest_surface.blit(
            self.bg_left, (self.bg_left_rect.x, self.bg_left_rect.y - bg_height)
        )

        # Blit right background
        dest_surface.blit(self.bg_right, self.bg_right_rect)
        dest_surface.blit(
            self.bg_right, (self.bg_right_rect.x, self.bg_right_rect.y - bg_height)
        )
