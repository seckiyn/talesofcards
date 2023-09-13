"""
    Classes and functions about cards
"""
import os
import sys
import pygame
from pygame import  sprite, image
from os.path import join
from lprint import print_error, print_debug, red, green, blue
from tools import interpret_file




PLACEHOLDER_CARD = join("cards", "card.png")

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
    @classmethod
    def from_toc(cls, filename):
        """
            Construct list of cards from toc file
        """
        from_cards = list()
        interpreter_object = interpret_file(filename)
        glob_vars = interpreter_object.global_variables
        cards = glob_vars["Cards"]
        default_command = None
        default_gameaction = lambda *args, **kwargs: None # Void func
        for card in cards.items():
            card_name: str
            card: dict
            card_name, card = card
            name = card["name"]
            image = card["image"]
            command = card.get("command", default_command)
            gameaction = card.get("gameaction", default_gameaction)
            new_card = cls(name, image, command=command, gameaction=gameaction)
            from_cards.append(new_card)
        return from_cards


# print(Card.from_toc("try.toc"))


class TocBaseException(Exception):
    __module__ = "builtins"


class WrongCommandException(TocBaseException):
    ...

class ArgumentException(TocBaseException):
    ...

class TooManyArgumentsException(ArgumentException):
    ...

class GameContainer:
    def __init__(self, width, height, health=100, shield=100):
        self.width = width
        self.height = height
        self.health = health
        self.shield = shield
        self.ALL_COMMANDS = ("SETHEALTH", "SETSHIELD", "GETHEALTH") #TODO: Change this into enum
    def execute_card(self, card: Card):
        """
            command consists of tuples of COMMAND:ARGS
            ex:
                command = [("SETHEALTH", 20), ("SETSHIELD", 20)]
        """
        command_list = card.gameaction
        for command in command_list:
            command_name, command_args = command
            self.handle_command(command_name, command_args)
    def handle_command(self, command_name, command_args):
        if command_name not in self.ALL_COMMANDS:
            raise WrongCommandException(f"There's no command called {command_name}")
        assert len(self.ALL_COMMANDS) == 3
        if command_name == "SETHEALTH":
            if len(command_args) != 1:
                raise TooManyArgumentsException("SETHEALTH exception needs only one argument!")
            to_set = command_args[0]
            if not isinstance(to_set, int):
                raise ArgumentException("SETHEALTH needs a INTEGER")
            self.set_health(to_set)
        if command_name == "SETSHIELD":
            if len(command_args) != 1:
                raise TooManyArgumentsException("SETSHIELD exception needs only one argument!")
            to_set = command_args[0]
            if not isinstance(to_set, int):
                raise ArgumentException("SETSHIELD needs a INTEGER")
            self.set_shield(to_set)
        if command_name == "GETHEALTH":
            ...



    def do_command(self, command_name, *args):
        ...
    def set_health(self, new_health: int):
        self.health = new_health
        self.healthsprite.set_health(new_health)
    def set_shield(self, new_shield: int):
        self.shield = new_shield
        self.shieldsprite.set_shield(new_shield)

class HealthSprite(pygame.sprite.Sprite):
    def __init__(self, game_container: GameContainer, fontname="", fontsize=80):
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
        self.image = self.my_font.render(str(self.health), True, "lightgreen")
        self.rect = self.image.get_rect()
        self.place_health()


class ShieldSprite(pygame.sprite.Sprite):
    def __init__(self, game_container: GameContainer, fontname="", fontsize=80):
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
        self.image = self.my_font.render(str(self.shield), True, "white")
        self.rect = self.image.get_rect()
        self.place_shield()

def tests():
    # Test handle command if it throws an error
    try:
        game_container = GameContainer(1,1)
        game_container.handle_command("doesn't exists", (12, 32, 45))
        print_debug(red("Didn't pass"))
    except WrongCommandException:
        print_debug(green("Passed"))

    test_game_actions = [
            ("SETHEALTH", (80,)),
            ("SETSHIELD", (10,))
            ]
    card = Card("my_card", "./cards/bomb.png", command=None, gameaction=test_game_actions)
    game_container = GameContainer(1, 1)

    mocksprite = lambda *args, **kwargs : None
    mocksprite.set_health = lambda *args, **kwargs : None
    mocksprite.set_shield = lambda *args, **kwargs : None
    game_container.healthsprite = mocksprite
    game_container.shieldsprite = mocksprite

    game_container.execute_card(card)
    if game_container.health == 80:
        print_debug(green("Passed"))
    else:
        print_debug(red("Didn't pass"))
    if game_container.shield == 10:
        print_debug(green("Passed"))
    else:
        print_debug(red("Didn't pass"))




if __name__ == "__main__":
    tests()
