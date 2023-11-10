"""Traffic Evader. A game made with pygame"""

import sys
import pygame
from sprites import Player, Background
from managers import FontManager
from config import WIDTH, HEIGHT, FPS

class View():
    """A base class for all game views with a game loop"""
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.active = True

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


class Game(View):
    """Main game view class"""
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Traffic Evader")

        self.player = Player((25, 225))
        self.background = Background()

        self.fonts = FontManager()

    def process_input(self) -> None:
        """Process game inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self) -> None:
        """Update: Move sprites, change state variables, etc"""


    def render(self) -> None:
        """Render: Fill background, blit sprites, etc"""
        self.screen.fill((255, 255, 255))

        self.background.draw(self.screen)
        self.player.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    Game().run()
