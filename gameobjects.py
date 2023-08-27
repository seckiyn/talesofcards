"""
    Classes and functions about cards
"""
import os
import sys
import pygame
from pygame import  sprite, image
from os.path import join
from lprint import print_error



PLACEHOLDER_CARD = join("cards", "card.png")

GAMEACTION = [
        ("SETHEALTH", 80),
        ("GETHEALTH", None)
        ]
class Card(sprite.Sprite):
    """
        A class to contain Cards
    """
    def __init__(self,
                 name="card",
                 imagepath=PLACEHOLDER_CARD, *,
                 command=None,
                 gameaction=lambda:1):
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

class GameContainer:
    def __init__(self, width, height, health=100, shield=100):
        self.width = width
        self.height = height
        self.health = health
        self.shield = shield
    def do_command(self, command_name, *args):
        ...
    def set_health(self, new_health):
        self.health = new_health
        self.healthsprite.set_health(new_health)
    def set_shield(self, new_shield):
        self.shield = new_shield
        self.shieldsprite.set_shield(new_shield)

class HealthSprite(pygame.sprite.Sprite):
    def __init__(self, game_container: GameContainer, fontname="", fontsize=30):
        pygame.sprite.Sprite.__init__(self)
        self.game_container = game_container
        self.game_container.healthsprite = self
        self.width = self.game_container.width
        self.height = self.game_container.height
        self.health = self.game_container.health
        self.my_font = pygame.font.SysFont(fontname, fontsize)
        self.image = self.my_font.render(str(self.health), True, "lightgreen")
        self.rect = self.image.get_rect()
    def place_health(self):
        y = 5*(self.height // 12)
        x = self.width // 8
        self.rect.center = (x, y)
    def set_health(self, new_health: int):
        self.health = self.game_container.health
        print(f"{self.health=}")
        self.image = self.my_font.render(str(self.health), True, "lightgreen")
        self.rect = self.image.get_rect()
        self.place_health()


class ShieldSprite(pygame.sprite.Sprite):
    def __init__(self, game_container: GameContainer, fontname="", fontsize=30):
        pygame.sprite.Sprite.__init__(self)
        self.game_container = game_container
        self.game_container.shieldsprite = self
        self.width = self.game_container.width
        self.height = self.game_container.height
        self.shield = self.game_container.shield
        self.my_font = pygame.font.SysFont(fontname, fontsize)
        self.image = self.my_font.render(str(self.shield), True, "white")
        self.rect = self.image.get_rect()
    def place_shield(self):
        y = 7*(self.height // 12)
        x = self.width // 8
        self.rect.center = (x, y)
    def set_shield(self, new_shield: int):
        self.shield = self.game_container.shield
        print(f"{self.shield=}")
        self.image = self.my_font.render(str(self.shield), True, "white")
        self.rect = self.image.get_rect()
        self.place_shield()
