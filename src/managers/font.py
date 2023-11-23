"""Font manager"""

import pygame

class FontManager():
    """Class storing game fonts"""
    def __init__(self) -> None:
        self.font_title = pygame.font.Font("./src/fonts/PublicPixel.woff", 38)
        self.font_score = pygame.font.Font("./src/fonts/PublicPixel.woff", 26)
        self.font_button = pygame.font.Font("./src/fonts/PublicPixel.woff", 16)
