#!/usr/bin/env python3
"""
    Pygame UI for the game
"""
import pygame
from lprint import red, green, blue, yellow
from random import choice as c
from parser import Parser
from lexer import Lexer
from typing import Tuple, Iterable
from pygame import Rect
from interpreter import Interpreter
from gameobjects import Card, GameContainer, HealthSprite, ShieldSprite, tests
from pygameutils import draw_guide_lines, draw_line, spread_card, adjust_surfaces
from config import WIDTH, HEIGHT, WINDOW_SIZE, Sprite, FPS

pygame.init()
pygame.font.init()


# Screen Setup #TODO: Add these to a config file






# Pygame #TODO: Add these to the GAME_CONTAINER class to easily




def create_gui() -> Tuple[Sprite, Sprite]:
    """
        Will return health and shield sprites
    """
    return 34 + 35

class Game(Interpreter):
    """
        Start the game
    """
    def __init__(self, gamescript="try.toc"):
        with open(gamescript) as f:
            parser = Parser(Lexer(f.read()))
        Interpreter.__init__(self, parser)
        self.interpret()
        self.running = True
        self.cards = self.extract_cards()
        print([i.gameaction for i in self.cards])
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.sprite_group = pygame.sprite.Group()
        self.board_sprite_group = pygame.sprite.Group()
        self.gui_sprite_group = pygame.sprite.Group()
        self.dead_sprite_group = pygame.sprite.Group()

        health = self.global_variables["Health"]
        shield = self.global_variables["Shield"]

        self.game_container = GameContainer(WIDTH, HEIGHT, health, shield)

    def extract_cards(self):
        """
            Construct list of cards from toc file
        """
        from_cards = list()
        cards = self.global_variables["Cards"]
        default_command = None
        default_gameaction = ""
        for card in cards.items():
            card_name: str
            card: dict
            card_name, card = card
            name = card["name"]
            image = card["image"]
            command = card.get("command", default_command)
            gameaction = card.get("gameaction", default_gameaction)
            new_card = Card(name, image, command=command, gameaction=gameaction)
            from_cards.append(new_card)
        print(green(from_cards))
        return from_cards
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_k:
                    if self.card_count < 8:
                        cardname = c(['bomb', 'card', 'card2'])
                        imagepath = f"./cards/{cardname}.png"
                        tmp_card = Card("bomb", imagepath)
                        self.sprite_group.add(tmp_card)
                    self.card_count += 1
                if event.key == pygame.K_m:
                    self.game_container.set_health(game_container.health - 10)
            if event.type == pygame.MOUSEBUTTONUP:
                """
                    Iterate over sprite_group
                        Check if position is inside the rect
                            Yes
                                Call the command function of card
                            No
                                Continue
                """
                mouse_pos = event.pos
                for mcard in self.sprite_group:
                    if mcard.check_mouse_up(mouse_pos):
                        self.click_event_player(mcard)

    def init_gui(self):
        # Health related
        health = HealthSprite(self.game_container)
        health.place_health()
        # Shield related
        shield = ShieldSprite(self.game_container)
        shield.place_shield()
        # Pack Gui
        self.gui_sprite_group.add(health)
        self.gui_sprite_group.add(shield)
        # Health related
#         health = HealthSprite(self.game_container)
#         health.place_health()
#         # Shield related
#         shield = ShieldSprite(self.game_container)
#         shield.place_shield()
        # Pack Gui
        self.gui_sprite_group.add(health)
        self.gui_sprite_group.add(shield)

    def handle_game_action(self, gameaction):
        print(type(gameaction))
        self.evaluate(gameaction)
        print(self.global_variables)

    def start(self):

        self.card_count = len(self.cards)
        [self.sprite_group.add(card) for card in self.cards]

        self.init_gui()


        while self.running:
            # Flush the screen
            self.screen.fill("darkred")
            # handle input
            self.handle_input()

            self.update()
            # redraw
            adjust_surfaces(self.sprite_group)
            self.sprite_group.draw(self.screen)
            # print(board_sprite_group) # TODO: Draw and adjust if needed
            self.board_sprite_group.draw(self.screen)
            self.gui_sprite_group.draw(self.screen)
            # draw_circles(screen, spread_card(5, WIDTH))
            # draw_rects(screen, spread_card(card_count, WIDTH))
            draw_guide_lines(self.screen)
            pygame.display.flip()

            delta_time = self.clock.tick(FPS) / 1000

    def update(self):
        self.game_container.set_health(int(self.global_variables["Health"]))
        self.game_container.set_shield(int(self.global_variables["Shield"]))
    def click_event_player(self, card: Card):
        """
            What to do when player clicks a card sprite
        """
        self.dead_sprite_group.add(*self.board_sprite_group)
        self.board_sprite_group.empty()
        card.kill()
        card.move_to(WIDTH//2, HEIGHT//2)
        print(red("GAAAAAAAAAAAAAAME         ACTION"), card.gameaction)
        if card.gameaction:
            self.handle_game_action(card.gameaction)
        self.board_sprite_group.add(card)


if __name__ == "__main__":
    game = Game()
    game.start()
