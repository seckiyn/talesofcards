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

        if command:
            self.command = command
        self.gameaction = gameaction
        self.to_update = list()
    def command(self, *args, **kwargs):
        print(f"My name is {self.name}")
    def move_to(self, x, y):
        self.rect.center = (x, y)

    def update(self):
        ...
    def check_mouse_up(self, mouse_pos, *args, **kwargs):
        if self.rect.collidepoint(mouse_pos):
            return True

