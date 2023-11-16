"""Game managers for Traffic Evader"""

import sys
import pygame
from src.views import View

class FontManager():
    """Class storing game fonts"""
    def __init__(self) -> None:
        self.font_title = pygame.font.Font("./src/fonts/PublicPixel.woff", 38)
        self.font_button = pygame.font.Font("./src/fonts/PublicPixel.woff", 16)

class ViewManager():
    """A class managing what view is displayed.
    The constructor needs a non-instantiated View class which will be the first view shown."""
    def __init__(self, init_view: type[View]) -> None:
        self.state = {
            "difficulty": "normal",
            "difficulty_index": (0, 0),
            "car": "blue_car",
            "car_index": (0, 0)
        }
        self.current_view = init_view(self.state)

        self.show_view(self.current_view)

    def show_view(self, view: View) -> None:
        """Display a view.
        Transitions to new view if one is set when the initial view isn't active anymore."""
        view.run()

        if view.transition_to:
            self.show_view(view.transition_to)
        else:
            pygame.quit()
            sys.exit()
