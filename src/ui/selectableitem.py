"""UI selectable item"""

from typing import Optional
import pygame
from src.storage import Fonts


class SelectableItem:
    """An item which can be chosen by clicking on it.
    Includes own item image/rect and a background around it."""

    def __init__(
        self,
        item_id: str,
        img_path: Optional[str] = None,
        button_text: Optional[str] = None,
        size: tuple[int, int] = (100, 100),
    ) -> None:
        self.item_id = item_id
        self.image = pygame.surface.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        if img_path:
            self.item_img = pygame.image.load(img_path).convert_alpha()
            self.item_img = pygame.transform.scale(
                self.item_img, (size[0] * 0.8, size[0] * 0.8)
            )
        elif button_text:
            self.item_img = Fonts().font_button.render(button_text, True, "black")
        else:
            raise TypeError(
                "Either img_path or button_text must be provided when instantiating SelectableItem"
            )

        self.item_rect = self.item_img.get_rect(center=self.rect.center)

    def draw(self, dest_surface: pygame.Surface, is_active: Optional[bool] = None):
        """Draw this SelectableItem onto dest_surface.
        If the item is set as active, the background will be gray."""
        if is_active:
            self.image.fill((75, 75, 75, 80))
        else:
            self.image.fill((0, 0, 0, 0))

        self.image.blit(self.item_img, self.item_rect)
        return dest_surface.blit(self.image, self.rect)
