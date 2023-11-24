"""Sound manager"""

import pygame

class Sounds():
    """Class storing game sounds"""
    def __init__(self) -> None:
        self.coin = pygame.mixer.Sound("./src/sounds/coin.wav")
        self.explosion = pygame.mixer.Sound("./src/sounds/explosion.wav")
        self.click = pygame.mixer.Sound("./src/sounds/menu_click.wav")
        self.click_deny = pygame.mixer.Sound("./src/sounds/menu_deny.wav")

        self.coin.set_volume(0.3)
        self.explosion.set_volume(0.3)
        self.click.set_volume(0.5)
        self.click_deny.set_volume(0.5)
