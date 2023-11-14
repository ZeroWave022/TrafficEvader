"""Game managers for Traffic Evader"""

import pygame

class FontManager():
    """Class storing game fonts"""
    def __init__(self) -> None:
        self.font_title = pygame.font.Font("./fonts/PublicPixel.woff", 38)
        self.font_button = pygame.font.Font("./fonts/PublicPixel.woff", 16)
