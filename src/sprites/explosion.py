"""Explosion sprite"""

import pygame
from src.utils import asset_path
from .gameobject import GameObject


class Explosion(GameObject):
    """Explosion sprite class"""

    def __init__(self) -> None:
        super().__init__(asset_path("sprites/explosion.png"), (640, 80))

        self._sheet_img = self.image
        self._sheet_rect = self.rect

        self.image = pygame.surface.Surface((80, 80), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(self._sheet_img, (0, 0), self.rect)

        self._frame_counter = 0
        self._sprite_frames = self._sheet_rect.width // self.rect.width
        self._current_sprite = 1
        self.animation_finished = False

    def update(self) -> None:
        """Updates explosion sprite, shows next animation frame"""
        self._frame_counter += 1
        if self._frame_counter >= 12:
            self._frame_counter = 0
            self._current_sprite += 1

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self._sheet_img, (0, 0), (self._current_sprite * 80, 0, 80, 80))

        if self._current_sprite >= self._sprite_frames:
            self.animation_finished = True
