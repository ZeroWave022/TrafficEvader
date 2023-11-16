"""Traffic Evader. A game made with pygame"""

import pygame
from views import Menu
from managers import ViewManager


if __name__ == "__main__":
    pygame.init()
    ViewManager(Menu)
