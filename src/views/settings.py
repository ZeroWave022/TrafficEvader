"""Game settings view"""

import pygame
from src.views.view import View
from src.ui import Button, SelectableItem, ItemSelector
from src.config import WIDTH, HEIGHT
from src.utils import asset_path


class Settings(View):
    """Game settings view class"""

    def __init__(self, state: dict) -> None:
        super().__init__(state)

        self.cars = [
            [
                SelectableItem(
                    "racing-blue-car.png",
                    asset_path("sprites/cars/racing-blue-car.png"),
                    size=(80, 80),
                ),
                SelectableItem(
                    "classic-blue-car.png",
                    asset_path("sprites/cars/classic-blue-car.png"),
                    size=(80, 80),
                ),
                SelectableItem(
                    "NES-car.png", asset_path("sprites/cars/NES-car.png"), size=(80, 80)
                ),
                SelectableItem(
                    "NES-police-car.png",
                    asset_path("sprites/cars/NES-police-car.png"),
                    size=(80, 80),
                ),
            ]
        ]

        self.car_selector = ItemSelector(self.cars, self.state["car_index"])
        self.car_selector.rect.x = (WIDTH - self.car_selector.rect.width) // 2
        self.car_selector.rect.y = 250

        self.difficulties = [
            [
                SelectableItem("easy", button_text="Easy", size=(125, 50)),
                SelectableItem("normal", button_text="Normal", size=(125, 50)),
                SelectableItem("hard", button_text="Hard", size=(125, 50)),
            ]
        ]

        diff_indexes = {"easy": 0, "normal": 1, "hard": 2}

        self.diff_selector = ItemSelector(
            self.difficulties, (0, diff_indexes[self.state["difficulty"]])
        )
        self.diff_selector.rect.x = (WIDTH - self.diff_selector.rect.width) // 2
        self.diff_selector.rect.y = 150

        self.back = Button(
            (WIDTH // 2 - 110, HEIGHT - 150, 220, 50), text="Back to Menu"
        )

    def _set_state(self) -> None:
        """Updates the state.
        Use it before the state is passed onto the next view."""
        self.state["difficulty"] = self.diff_selector.active_item.item_id
        self.state["car"] = self.car_selector.active_item.item_id
        self.state["car_index"] = self.car_selector.get_active_item_index()

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.diff_selector.process_input(mouse_pos)
                self.car_selector.process_input(mouse_pos)
                self.back.click_event()

        if self.back.clicked:
            self._set_state()
            self.active = False
            self.transition_to = "menu"

    def render(self) -> None:
        self.screen.fill((255, 255, 255))

        self.diff_selector.draw(self.screen)
        self.car_selector.draw(self.screen)
        self.back.draw(self.screen)

        pygame.display.flip()
