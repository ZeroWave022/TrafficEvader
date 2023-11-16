"""UI elements for Traffic Evader"""

from typing import Optional
import pygame
from src.managers import FontManager

class Button:
    def __init__(
        self,
        rect_value: tuple[int, int, int, int],
        color: tuple[int, int, int] | str = "gray",
        text: Optional[str] = None
    ) -> None:
        self.rect = pygame.rect.Rect(*rect_value)
        self.color = color
        self.clicked = False
        self.text = text
        self.fonts = FontManager()

    def click_event(self):
        """Handles a click event in game loop iteration.
        Call whenever a click event happens."""
        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            self.clicked = True

    def draw(self, dest_surface: pygame.Surface):
        """Draw this button onto dest_surface."""
        pygame.draw.rect(dest_surface, self.color, self.rect)

        if self.text:
            rendered_text = self.fonts.font_button.render(self.text, True, "black")
            dest_surface.blit(rendered_text, rendered_text.get_rect(center=self.rect.center))

class SelectableItem():
    """An item which can be chosen by clicking on it."""
    def __init__(
            self,
            item_id: str,
            img_path: Optional[str] = None,
            button_text: Optional[str] = None,
            size: tuple[int, int] = (100, 100)
        ) -> None:
        self.item_id = item_id
        self.image = pygame.surface.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        if img_path:
            self.item_img = pygame.image.load(img_path).convert_alpha()
            self.item_img = pygame.transform.scale(self.item_img, (size[0] * 0.8, size[0] * 0.8))
        elif button_text:
            self.item_img = FontManager().font_button.render(button_text, True, "black")
        else:
            raise TypeError(
                "Either img_path or button_text must be provided when instantiating SelectableItem"
            )

        self.item_rect = self.item_img.get_rect(center=self.rect.center)

    def draw(self, dest_surface: pygame.Surface, is_active: Optional[bool] = None):
        if is_active:
            self.image.fill((75, 75, 75, 80))
        else:
            self.image.fill((0, 0, 0, 0))

        self.image.blit(self.item_img, self.item_rect)
        return dest_surface.blit(self.image, self.rect)

class ItemSelector():
    """Creates a row of SelectableItems and stores current choice.
    
    grid_rows: list[list[SelectableItem]]
        A list of rows (a list each) of SelectableItems which can be chosen.
        Assumes all SelectableItems are of same size, and that all rows have the same amount of items.
    init_active: tuple[int, int]
        A tuple with two indexes (row, column) of the initially active item."""

    def __init__(self, grid_rows: list[list[SelectableItem]], init_active: tuple[int, int]) -> None:
        self.rows = grid_rows
        self.items_width = self.rows[0][0].rect.width
        self.items_height = self.rows[0][0].rect.height

        self.image = pygame.surface.Surface(
            (
                self.items_width * len(self.rows[0]) + (len(self.rows[0]) - 1) * 50,
                self.items_height * len(self.rows) + (len(self.rows) - 1) * 25
            ),
            pygame.SRCALPHA
        )
        self.rect = self.image.get_rect()

        self.active_item = self.rows[init_active[0]][init_active[1]]

        self.set_item_positions()

    def set_item_positions(self) -> None:
        row_y = 0
        for row in self.rows:
            x_pos = 0
            for item in row:
                item.rect.x = x_pos
                item.rect.y = row_y
                x_pos += self.items_width + 50

            row_y += self.items_height + 25

    def get_active_item_index(self):
        for row_id, row in enumerate(self.rows):
            currently_selected = next((i for i in row if i == self.active_item), None)
            if currently_selected is not None:
                return (row_id, row.index(currently_selected))

        raise RuntimeError("Index of active item in ItemSelector could not be found")

    def process_input(self, position: tuple[int, int]) -> None:
        if not self.rect.collidepoint(position):
            return

        # Find relative coordinates where the user clicked inside the ItemSelector surface
        relative_x = position[0] - self.rect.x
        relative_y = position[1] - self.rect.y

        for row in self.rows:
            for item in row:
                if item.rect.collidepoint(relative_x, relative_y):
                    self.active_item = item
                    break


    def draw(self, dest_surface: pygame.Surface):
        self.image.fill((0, 0, 0, 0))
        self.active_item.draw(self.image, True)

        for row in self.rows:
            for item in row:
                item.draw(self.image)

        dest_surface.blit(self.image, self.rect)
