"""Player sprite"""

from typing import Literal
from src.config import LANE_SWITCH_SPEED
from .gameobject import GameObject


class Player(GameObject):
    """Class managing the player"""

    def __init__(self, img_path: str, level: dict) -> None:
        super().__init__(img_path, (75, 75))

        self.level_info = level

        self.rect.x = self.level_info["player"]["init_x"]
        self.rect.y = 400

        self.lane = self.level_info["player"]["init_lane"]
        self.switching_lane: Literal["left", "right", False] = False
        self._switch_frames = round(15 / LANE_SWITCH_SPEED)
        self._lane_delta_x = round(self.level_info["lane_width"] / self._switch_frames)
        self._moving_to = 0

    def move_left(self) -> None:
        """Initiate a lane switch.
        The movement itself is handled later, in update()."""
        if not self.switching_lane and self.lane - 1 >= 1:
            self.switching_lane = "left"
            self.lane -= 1
            self._moving_to = self.rect.centerx - self.level_info["lane_width"]

    def move_right(self) -> None:
        """Initiate a lane switch.
        The movement itself is handled later, in update()."""
        if not self.switching_lane and self.lane + 1 <= self.level_info["lanes"]:
            self.switching_lane = "right"
            self.lane += 1
            self._moving_to = self.rect.centerx + self.level_info["lane_width"]

    def update(self) -> None:
        """Move player for new frame"""
        if self.switching_lane == "left":
            # Only move player by delta_x if it won't move it too far (inaccuracy caused by rounding)
            if self.rect.centerx - self._lane_delta_x > self._moving_to:
                self.rect.centerx -= self._lane_delta_x
            else:
                self.rect.centerx = self._moving_to
                self.switching_lane = False

        if self.switching_lane == "right":
            # Only move player by delta_x if it won't move it too far (inaccuracy caused by rounding)
            if self.rect.centerx + self._lane_delta_x < self._moving_to:
                self.rect.centerx += self._lane_delta_x
            else:
                self.rect.centerx = self._moving_to
                self.switching_lane = False
