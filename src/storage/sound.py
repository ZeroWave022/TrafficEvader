"""Sound manager"""

from sys import platform as sys_platform
import pygame
from src.utils import asset_path


class Sounds:
    """Class storing game sounds"""

    def __init__(self) -> None:
        if sys_platform == "emscripten":
            self.file_extension = "ogg"
        else:
            self.file_extension = "wav"

        self.coin = pygame.mixer.Sound(asset_path(f"sounds/coin.{self.file_extension}"))
        self.explosion = pygame.mixer.Sound(
            asset_path(f"sounds/explosion.{self.file_extension}")
        )
        self.click = pygame.mixer.Sound(
            asset_path(f"sounds/menu_click.{self.file_extension}")
        )
        self.click_deny = pygame.mixer.Sound(
            asset_path(f"sounds/menu_deny.{self.file_extension}")
        )

        self.coin.set_volume(0.3)
        self.explosion.set_volume(0.3)
        self.click.set_volume(0.5)
        self.click_deny.set_volume(0.5)
