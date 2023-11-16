"""Traffic Evader. A game made with pygame"""

import pygame
from src.views.menu import Menu
from src.managers import ViewManager


if __name__ == "__main__":
    pygame.init()
    ViewManager(Menu)
