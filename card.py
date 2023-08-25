"""
    Classes and functions about cards
"""
import os
import sys
from pygame import  sprite, image
from os.path import join
from lprint import print_error

PLACEHOLDER_CARD = join("cards", "card.png")

class Card(sprite.Sprite):
    """
        A class to contain Cards
    """
    def __init__(self,
                 name="card",
                 imagepath=PLACEHOLDER_CARD, *,
                 command=None,
                 gameaction=None):
        sprite.Sprite.__init__(self)
        self.name = name
        self.imagepath = imagepath

        self.image = image.load(self.imagepath)
        self.rect = self.image.get_rect()
        if not os.path.exists(imagepath):
            print_error(f"{imagepath} doesn't exists")
            sys.exit()

        self.command = command
        self.command = lambda: print(f"My name is {self.name}")
        self.gameaction = gameaction
    def check_mouse_up(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.command()

