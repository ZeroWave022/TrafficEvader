"""View manager"""

import sys
import pygame
from src.views import View, Game, GameOver, Menu, Settings

class ViewManager():
    """A class managing what view is displayed.
    The constructor needs a non-instantiated View class which will be the first view shown."""
    def __init__(self) -> None:
        self.state = {
            "difficulty": "normal",
            "difficulty_index": (0, 0),
            "car": "blue_car.png",
            "car_index": (0, 0)
        }
        self.views = {
            "game": Game,
            "gameover": GameOver,
            "menu": Menu,
            "settings": Settings
        }

        self.current_view = Menu(self.state)

        self.show_view(self.current_view)

    def show_view(self, view: View) -> None:
        """Display a view.
        Transitions to new view if one is set when the initial view isn't active anymore."""
        view.run()

        if view.transition_to:
            # Get the View class we're transitioning to
            move_to = self.views[view.transition_to]
            self.show_view(move_to(view.state))
        else:
            pygame.quit()
            sys.exit()
