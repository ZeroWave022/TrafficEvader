"""Traffic Evader. A game made with pygame"""

import sys
import pygame
from views import View, Menu

class ViewManager():
    """A class managing what view is displayed"""
    def __init__(self, init_view: View) -> None:
        self.current_view = init_view

        self.show_view(init_view)

    def show_view(self, view: View) -> None:
        """Display a view.
        Transitions to new view if one is set when the initial view isn't active anymore."""
        view.run()

        if view.transition_to:
            self.show_view(view.transition_to)
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    pygame.init()
    ViewManager(Menu())
