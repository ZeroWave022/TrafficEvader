"""Game managers for Traffic Evader"""

import pygame

class FontManager():
    """Class storing game fonts"""
    def __init__(self) -> None:
        self.font_title = pygame.font.SysFont("calibri", 42)
        self.font_button = pygame.font.SysFont("calibri", 24)
