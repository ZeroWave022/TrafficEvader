"""Coin sprite"""

import pygame
from src.utils import asset_path
from .gameobject import GameObject

class Coin(GameObject):
    def __init__(self, position: tuple[int, int], lane: int) -> None:
        super().__init__(asset_path("sprites/coin.png"), (160, 32))

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
