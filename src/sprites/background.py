"""Background sprite"""

import pygame
from src.config import WIDTH, HEIGHT
from src.utils import asset_path
from .gameobject import GameObject

class Background(GameObject):
    """Class managing game background"""
    def __init__(self, level: dict) -> None:
        lanes_num = level['lanes']
        super().__init__(asset_path(f"sprites/road_{lanes_num}.png"))

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
