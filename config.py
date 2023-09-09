from typing import Tuple
import pygame

WIDTH: int = 1500
HEIGHT: int = 750
WINDOW_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)
FPS = 60


class Sprite(pygame.sprite.Sprite):
    def __init__(self, imagepath: str):
        """
            Base Sprite class
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
