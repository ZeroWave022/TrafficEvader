"""Game over view"""

import pygame
from src.views.view import View
from src.ui import Button
from src.config import WIDTH, HEIGHT

class GameOver(View):
    """Game over view class"""
    def __init__(self, state: dict) -> None:
        super().__init__(state)

        self.title = self.fonts.font_title.render("Game Over", True, "black", (255, 255, 255))

        self.retry = Button((WIDTH // 2 - 110, HEIGHT // 2 - 120, 220, 50), text="Retry")
        self.back = Button((WIDTH // 2 - 110, HEIGHT // 2 - 60, 220, 50), text="Back to Menu")
        self.exit_btn = Button((WIDTH // 2 - 110, HEIGHT // 2, 220, 50), text="Exit")

        self.buttons = [self.retry, self.back, self.exit_btn]

        self.overlay = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((50, 50, 50, 150))
        self.overlay_blitted = False

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click_event()

        if self.retry.clicked or self.back.clicked:
            self.active = False

        if self.retry.clicked:
            self.transition_to ="game"

        if self.back.clicked:
            self.transition_to = "menu"

        if self.exit_btn.clicked:
            self.exit()

    def render(self) -> None:
        if not self.overlay_blitted:
            self.screen.blit(self.overlay, (0, 0))
            self.overlay_blitted = True

        for button in self.buttons:
            button.draw(self.screen)
        
        self.screen.blit(self.title, ((WIDTH - self.title.get_width()) // 2, HEIGHT - 450))

        pygame.display.flip()
