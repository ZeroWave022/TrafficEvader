"""Traffic Evader. A game made with pygame"""

import sys
import pygame
from views import View, Menu


class ViewManager():
    """A class managing what view is displayed.
    The constructor needs a non-instantiated View class which will be the first view shown."""
    def __init__(self, init_view: type[View]) -> None:
        self.state = {}
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

if __name__ == "__main__":
    pygame.init()
    ViewManager(Menu)
