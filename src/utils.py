"""Varius utilities which don't fit any other submodule"""

from pathlib import Path

def asset_path(file_path: str) -> str:
    """Prepares an absolute path string to an asset.
    
    Examples (on Windows):
    asset_path("sprites/coin.png") -> C:/.../src/assets/sprites/coin.png
    asset_path("sprites/cars/blue_car.png") -> C:/.../src/assets/sprites/cars/blue_car.png"""

    assets_path = Path(__file__).parent.joinpath("./assets").resolve()

    return str(assets_path.joinpath(file_path))

