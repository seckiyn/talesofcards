#!/usr/bin/env python3
"""
    Pygame UI for the game
"""
import pygame
from random import choice as c
from typing import Tuple, Iterable
from pygame import Rect
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

class Game():
    """
        Start the game
    """
    def __init__(self):
        self.running = True
        self.cards = Card.from_toc("try.toc")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.sprite_group = pygame.sprite.Group()
        self.board_sprite_group = pygame.sprite.Group()
        self.gui_sprite_group = pygame.sprite.Group()
        self.dead_sprite_group = pygame.sprite.Group()

        self.game_container = GameContainer(WIDTH, HEIGHT)

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
                    print_debug(f"Before {self.game_container.health}")
                    self.game_container.set_health(game_container.health - 10)
                    print_debug(f"After {game_container.health}")
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

    def start(self):

        self.card_count = len(self.cards)
        [self.sprite_group.add(card) for card in self.cards]
        # Health related
        health = HealthSprite(self.game_container, fontsize=80)
        health.place_health()


        # Shield related
        shield = ShieldSprite(self.game_container, fontsize=80)
        shield.place_shield()

        # Pack Gui
        self.gui_sprite_group.add(health)
        self.gui_sprite_group.add(shield)

        # Health related
        health = HealthSprite(self.game_container, fontsize=80)
        health.place_health()


        # Shield related
        shield = ShieldSprite(self.game_container, fontsize=80)
        shield.place_shield()

        # Pack Gui
        self.gui_sprite_group.add(health)
        self.gui_sprite_group.add(shield)


        while self.running:
            # handle input


                    # proccess input
                    # remove screen
                    # blit


            # card = Card("card", "./cards/card.png")
            # card2 = Card("card2", "./cards/card2.png")
            # card2.rect.center = WIDTH // 2, HEIGHT // 2
            # sprite_group.add((card, card2))

            # Flush the screen
            self.screen.fill("darkred")




            # get input
            # handle input
            self.handle_input()
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

    def click_event_player(self, card: Card):
        """
            What to do when player clicks a card sprite
        """
        self.dead_sprite_group.add(*self.board_sprite_group)
        self.board_sprite_group.empty()
        card.kill()
        card.move_to(WIDTH//2, HEIGHT//2)
        # card.gameaction()
        self.board_sprite_group.add(card)


if __name__ == "__main__":
    game = Game()
    game.start()
