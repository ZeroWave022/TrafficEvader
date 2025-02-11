"""UI button"""

from typing import Optional
import pygame
from src.storage import Fonts, Sounds


class Button:
    """A UI button to handle user input"""

    def __init__(
        self,
        rect_value: tuple[int, int, int, int],
        color: tuple[int, int, int] | str = "gray",
        text: Optional[str] = None,
    ) -> None:
        self.rect = pygame.rect.Rect(*rect_value)
        self.color = color
        self.clicked = False
        self.text = text
        self.fonts = Fonts()
        self.sounds = Sounds()

    def click_event(self):
        """Handles a click event in game loop iteration.
        Call whenever a click event happens."""
        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            self.clicked = True
            self.sounds.click.play()

    def draw(self, dest_surface: pygame.Surface):
        """Draw this button onto dest_surface."""
        pygame.draw.rect(dest_surface, self.color, self.rect)

        if self.text:
            rendered_text = self.fonts.font_button.render(self.text, True, "black")
            dest_surface.blit(
                rendered_text, rendered_text.get_rect(center=self.rect.center)
            )
