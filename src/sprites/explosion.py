"""Explosion sprite"""

import pygame
from src.utils import asset_path
from .gameobject import GameObject

class Explosion(GameObject):
    def __init__(self) -> None:
        super().__init__(asset_path("sprites/explosion.png"), (640, 80))

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
