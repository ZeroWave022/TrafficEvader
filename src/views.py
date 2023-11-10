"""Traffic Evader views"""

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
                pygame.quit()
                sys.exit()

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
        self.play_button = pygame.draw.rect(
            self.screen,
            "gray",
            (WIDTH // 2 - 75, HEIGHT - 350, 150, 50)
        )

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if self.play_button.collidepoint(mouse_position):
                    self.active = False
                    self.transition_to = Game()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))

        pygame.draw.rect(
            self.screen,
            "gray",
            (WIDTH // 2 - 75, HEIGHT - 350, 150, 50)
        )

        title = self.fonts.font_title.render("Traffic Evader", True, "black")
        button_text = self.fonts.font_button.render("Play", True, "black")

        self.screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT - 450))
        self.screen.blit(button_text, button_text.get_rect(center=self.play_button.center))

        pygame.display.flip()
