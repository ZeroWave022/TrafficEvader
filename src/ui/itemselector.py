"""UI item selector"""

import pygame
from src.storage import Sounds
from .selectableitem import SelectableItem


class ItemSelector:
    """Creates a row of SelectableItems and stores current choice."""

    def __init__(
        self, grid_rows: list[list[SelectableItem]], init_active: tuple[int, int]
    ) -> None:
        """Instantiate an ItemSelector.

        grid_rows: list[list[SelectableItem]]
            A list of rows (a list each) of SelectableItems which can be chosen.
            Assumes all SelectableItems are of same size, and that all rows have the same amount of items.
        init_active: tuple[int, int]
            A tuple with two indexes (row, column) of the initially active item."""
        self.rows = grid_rows
        self.items_width = self.rows[0][0].rect.width
        self.items_height = self.rows[0][0].rect.height

        self.image = pygame.surface.Surface(
            (
                self.items_width * len(self.rows[0]) + (len(self.rows[0]) - 1) * 50,
                self.items_height * len(self.rows) + (len(self.rows) - 1) * 25,
            ),
            pygame.SRCALPHA,
        )
        self.rect = self.image.get_rect()

        self.active_item = self.rows[init_active[0]][init_active[1]]
        self.sounds = Sounds()

        self._set_item_positions()

    def _set_item_positions(self) -> None:
        """Sets up item positions in the grid."""
        row_y = 0
        for row in self.rows:
            x_pos = 0
            for item in row:
                item.rect.x = x_pos
                item.rect.y = row_y
                x_pos += self.items_width + 50

            row_y += self.items_height + 25

    def get_active_item_index(self) -> tuple[int, int]:
        """Retrieve the index of the active item."""
        for row_id, row in enumerate(self.rows):
            currently_selected = next((i for i in row if i == self.active_item), None)
            if currently_selected is not None:
                return (row_id, row.index(currently_selected))

        raise RuntimeError("Index of active item in ItemSelector could not be found")

    def process_input(self, position: tuple[int, int]) -> None:
        """Handle a click event for an ItemSelector."""
        if not self.rect.collidepoint(position):
            return

        # Find relative coordinates where the user clicked inside the ItemSelector surface
        relative_x = position[0] - self.rect.x
        relative_y = position[1] - self.rect.y

        for row in self.rows:
            for item in row:
                if item.rect.collidepoint(relative_x, relative_y):
                    if self.active_item == item:
                        self.sounds.click_deny.play()
                    else:
                        self.active_item = item
                        self.sounds.click.play()
                    break

    def draw(self, dest_surface: pygame.Surface) -> None:
        """Draw this ItemSelector onto dest_surface."""
        self.image.fill((0, 0, 0, 0))
        self.active_item.draw(self.image, True)

        for row in self.rows:
            for item in row:
                item.draw(self.image)

        dest_surface.blit(self.image, self.rect)
