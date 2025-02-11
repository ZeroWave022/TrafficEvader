"""A base game object class"""

import pygame


class GameObject(pygame.sprite.Sprite):
    """A base game object class for all sprites"""

    def __init__(
        self, img_path: str, scale: float | tuple[int, int] | None = None
    ) -> None:
        super().__init__()

        self.image = pygame.image.load(img_path).convert_alpha()

        if scale and isinstance(scale, float):
            self.image = pygame.transform.scale_by(self.image, scale)
        elif scale and isinstance(scale, tuple):
            self.image = pygame.transform.scale(self.image, scale)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, dest_surface: pygame.Surface):
        """Draw this sprite onto dest_surface."""
        return dest_surface.blit(self.image, self.rect)
