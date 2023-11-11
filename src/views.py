"""Traffic Evader views"""

import sys
import pygame
from sprites import Player, Background
from ui import Button
from managers import FontManager
from config import WIDTH, HEIGHT, FPS

class View():
    """A base class for all game views with a game loop"""
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.active = True
        self.transition_to: View | None = None

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


class Game(View):
    """Main game view class"""
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Traffic Evader")

        self.player = Player((WIDTH // 2 - 95, 400))
        self.background = Background()

        self.fonts = FontManager()

    def process_input(self) -> None:
        """Process game inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self) -> None:
        """Update: Move sprites, change state variables, etc"""
        self.background.update()
        self.player.update()


    def render(self) -> None:
        """Render: Fill background, blit sprites, etc"""
        self.screen.fill((255, 255, 255))

        self.background.draw(self.screen)
        self.player.draw(self.screen)

        pygame.display.flip()

class Menu(View):
    """Main menu view class"""
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Traffic Evader")

        self.fonts = FontManager()
        self.title = self.fonts.font_title.render("Traffic Evader", True, "black")

        self.play = Button((WIDTH // 2 - 75, HEIGHT - 350, 150, 50), text="Play")
        self.settings = Button((WIDTH // 2 - 75, HEIGHT - 290, 150, 50), text="Settings")
        self.exit_btn = Button((WIDTH // 2 - 75, HEIGHT - 230, 150, 50), text="Quit")

        self.buttons = [self.play, self.settings, self.exit_btn]

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click_event()

        if self.play.clicked:
            self.active = False
            self.transition_to = Game()

        if self.exit_btn.clicked:
            self.exit()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))

        for button in self.buttons:
            button.draw(self.screen)

        self.screen.blit(self.title, ((WIDTH - self.title.get_width()) // 2, HEIGHT - 450))

        pygame.display.flip()