"""Base view module"""

import sys
import pygame
from src.config import WIDTH, HEIGHT, FPS

class View():
    """A base class for all game views with a game loop"""
    def __init__(self, state: dict) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.active = True
        self.transition_to: View | None = None
        self.state = state

    def process_input(self) -> None:
        """Game loop part 1: Process game inputs.
        Override this method when inheriting."""

    def update(self) -> None:
        """Game loop part 2: Move sprites, change state variables, etc.
        Override this method when inheriting."""

    def render(self) -> None:
        """Game loop part 3: Fill background, blit sprites, etc.
        Override this method when inheriting.
        """

    def run(self):
        """Run game loop"""
        while self.active:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def exit(self):
        """Quit pygame and end python process"""
        pygame.quit()
        sys.exit()
