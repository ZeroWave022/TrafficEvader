"""Game menu view"""

import pygame
from src.views.view import View
from src.ui import Button
from src.managers import FontManager
from src.config import WIDTH, HEIGHT

import src.views.game as game
import src.views.settings as settings

class Menu(View):
    """Main menu view class"""
    def __init__(self, state: dict) -> None:
        super().__init__(state)
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
            self.transition_to = game.Game(self.state)

        if self.settings.clicked:
            self.active = False
            self.transition_to = settings.Settings(self.state)

        if self.exit_btn.clicked:
            self.exit()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))

        for button in self.buttons:
            button.draw(self.screen)

        self.screen.blit(self.title, ((WIDTH - self.title.get_width()) // 2, HEIGHT - 450))

        pygame.display.flip()
