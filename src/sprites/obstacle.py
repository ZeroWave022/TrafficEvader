"""Obstacle sprite"""

from random import randint, choice
from src.config import CARS_OBSTACLES
from src.utils import asset_path
from .gameobject import GameObject

class Obstacle(GameObject):
    def __init__(self, position: tuple[int, int], lane: int):
        self.img_path = self._select_random_car()
        super().__init__(self.img_path, (64, 64))

        self.rect.x = position[0]
        self.rect.y = position[1]
        self.lane = lane

    def _select_random_car(self) -> str:
        rand = randint(1, 100)

        if rand <= 60:
            chosen_car = choice(CARS_OBSTACLES["low"])
        elif rand <= 97:
            chosen_car = choice(CARS_OBSTACLES["medium"])
        else:
            chosen_car = choice(CARS_OBSTACLES["high"])

        return asset_path(f"sprites/obstacles/{chosen_car}")

    def update(self, speed: int):
        """Move obstacle for new frame"""
        self.rect.y += speed
