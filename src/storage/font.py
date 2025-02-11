"""Font manager"""

import pygame
from src.utils import asset_path


class Fonts:
    """Class storing game fonts"""

    def __init__(self) -> None:
        font_path = asset_path("fonts/PublicPixel.woff")

        self.font_title = pygame.font.Font(font_path, 38)
        self.font_score = pygame.font.Font(font_path, 26)
        self.font_button = pygame.font.Font(font_path, 16)
