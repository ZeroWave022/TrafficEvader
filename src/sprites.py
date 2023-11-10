"""Sprites for Traffic Evader"""

import pygame
from config import HEIGHT


class Player(pygame.sprite.Sprite):
    """Class managing the player"""
    def __init__(self, coords: tuple[int, int]) -> None:
        super().__init__()

        self._raw_image = pygame.image.load("./sprites/blue_car.png").convert_alpha()
        self.image = pygame.transform.scale_by(self._raw_image, 1.25)
        self.rect = self.image.get_rect()

        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def draw(self, dest_surface: pygame.Surface):
        """Draw this sprite onto dest_surface."""
        return dest_surface.blit(self.image, self.rect)


class Background(pygame.sprite.Sprite):
    """Class managing game background"""
    def __init__(self) -> None:
        super().__init__()

        self.surface = pygame.image.load("./sprites/road_3.png")
        self.rect = self.surface.get_rect()

        self.rect.x = (pygame.display.get_surface().get_width() - self.rect.width) // 2
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
        self.update()

        second_bg = self.rect.copy()
        second_bg.y -= second_bg.height

        dest_surface.blit(self.surface, self.rect)
        dest_surface.blit(self.surface, second_bg)
