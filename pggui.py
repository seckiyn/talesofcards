#!/usr/bin/env python3
"""
    Pygame UI for the game
"""
import pygame
from random import choice as c
from typing import Tuple, Iterable
from pygame import Rect
from gameobjects import Card, GameContainer, HealthSprite, ShieldSprite, tests

pygame.init()
pygame.font.init()


# Screen Setup
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


def draw_line(surface, cord1, cord2, width=3, color="purple"):
    """
        Draw lines for debug
    """
    pygame.draw.line(surface, color, cord1, cord2, width)


def draw_guide_lines(surface):
    """
        Draw guide lines for geometry
    """
    HALFWIDTH: int = WIDTH // 2
    THIRDHEIGHT: int = HEIGHT // 3
    # Board-Top Horizontal line
    cord1_x = 0
    cord1_y = THIRDHEIGHT
    cord2_x = WIDTH
    cord2_y = cord1_y
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2)

    # Board-Bottom Horizontal line
    cord1_x = 0
    cord1_y = 2 * THIRDHEIGHT
    cord2_x = WIDTH
    cord2_y = cord1_y
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2)

    # Opponent Card Guide Line
    cord1_x = 0
    cord1_y = THIRDHEIGHT // 2
    cord2_x = WIDTH
    cord2_y = cord1_y
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1)

    # Board Card Guide Line also horizontal center
    cord1_x = 0
    cord1_y = 3 * (THIRDHEIGHT // 2)
    cord2_x = WIDTH
    cord2_y = cord1_y
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1, "green")

    # Player Card Guide Line
    cord1_x = 0
    cord1_y = 5 * (THIRDHEIGHT // 2)
    cord2_x = WIDTH
    cord2_y = cord1_y
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1)

    # Center Vertical line
    cord1_x = HALFWIDTH
    cord1_y = 0
    cord2_x = cord1_x
    cord2_y = HEIGHT
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1, "green")

    # Left Vertical line
    cord1_x = HALFWIDTH // 2
    cord1_y = 0
    cord2_x = cord1_x
    cord2_y = HEIGHT
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1, "green")

    # Right Vertical line
    cord1_x = 3 * (HALFWIDTH // 2)
    cord1_y = 0
    cord2_x = cord1_x
    cord2_y = HEIGHT
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1, "green")

    # LeftSide-Left Vertical line
    cord1_x = (HALFWIDTH // 2) // 2
    cord1_y = 0
    cord2_x = cord1_x
    cord2_y = HEIGHT
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1, "lightblue")


    # Board-Bottom Horizontal line - Board Guide Line
    cord1_x = 0
    cord1_y = 7 * (THIRDHEIGHT // 4)
    cord2_x = WIDTH
    cord2_y = cord1_y
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1, color="lightblue")

    # Board-TOP Horizontal line - Board Guide Line
    cord1_x = 0
    cord1_y = 5 * (THIRDHEIGHT // 4)
    cord2_x = WIDTH
    cord2_y = cord1_y
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2, 1, color="lightblue")

def spread_card(card_count: int, size: float, cardsize=157, padding=10) -> Tuple[int, ...]:
    """
        Returns a tuple of x values to spread cards in hand
    """
    halfsize = size // 2
    halfpadding = padding // 2
    halfcardsize = cardsize // 2

    if card_count <= 0 or not isinstance(card_count, int):
        raise ValueError("Card count must be a positive integer")

    if card_count > 8:
        card_count = 8
    if card_count == 1:
        return (size // 2,)
    if card_count == 2:
        left = halfsize - halfpadding
        right = halfsize + halfpadding
        left = left - halfcardsize
        right = right + halfcardsize
        return left, right


    if card_count == 3:
        middle = halfsize
        left = halfsize - padding - cardsize
        right = halfsize + padding + cardsize
        return left, middle, right


    left, *middles, right = spread_card(card_count - 2, size)
    mostleft = left - padding - cardsize
    mostright = right + padding + cardsize
    return mostleft, left, *middles, right, mostright


def draw_circles(surface, x_cords: Tuple[int, ...]) -> None:
    """
        Drawing circle wrapper to be removed
    """
    for x_cord in x_cords:
        pygame.draw.circle(surface, "red", (x_cord, 5 * (HEIGHT // 6)), 157)


def draw_rects(surface, x_cords: Tuple[int, ...]) -> None:
    """
        Drawing rectangles wrapper to be removed
    """
    for x_cord in x_cords:
        width = 157
        height = 250
        rect = pygame.Rect(0, 0, width, height)
        rect.center = x_cord, 5 * (HEIGHT // 6)
        pygame.draw.rect(surface, "red", rect)


def adjust_surfaces(surface: pygame.Surface, surf: Iterable[Card]) -> None:
    """
        Takes the tuple of surfaces(surf) and adjusts them according to
        x values given by spread_card function
    """
    if not surf:
        return
    x_cords = spread_card(len(surf), WIDTH)
    for x_cord, card in zip(x_cords, surf):
        card.rect.center = x_cord, 5 * (HEIGHT // 6)


# Pygame #TODO: Add these to the GAME_CONTAINER class to easily
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
delta_time = 0
sprite_group = pygame.sprite.Group()
board_sprite_group = pygame.sprite.Group()
gui_sprite_group = pygame.sprite.Group()
dead_sprite_group = pygame.sprite.Group()
game_container = GameContainer(WIDTH, HEIGHT)



def click_event_player(card: Card):
    """
        What to do when player clicks a card sprite
    """
    dead_sprite_group.add(*board_sprite_group)
    board_sprite_group.empty()
    card.kill()
    card.move_to(WIDTH//2, HEIGHT//2)
    card.gameaction()
    board_sprite_group.add(card)

def create_gui() -> Tuple[Sprite, Sprite]:
    """
        Will return health and shield sprites
    """
    return 34 + 35

def Game() -> None:
    """
        Start the game
    """
    running = True
    # card = Card("card", "./cards/card.png")
    # card2 = Card("card2", "./cards/card2.png")
    # card2.rect.center = WIDTH // 2, HEIGHT // 2
    # sprite_group.add((card, card2))

    cards = Card.from_toc("try.toc")
    card_count = len(cards)
    [sprite_group.add(card) for card in cards]

    # Health related
    health = HealthSprite(game_container, fontsize=80)
    health.place_health()


    # Shield related
    shield = ShieldSprite(game_container, fontsize=80)
    shield.place_shield()

    # Pack Gui
    gui_sprite_group.add(health)
    gui_sprite_group.add(shield)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_k:
                    if card_count < 8:
                        cardname = c(['bomb', 'card', 'card2'])
                        imagepath = f"./cards/{cardname}.png"
                        tmp_card = Card("bomb", imagepath)
                        sprite_group.add(tmp_card)
                    card_count += 1
                if event.key == pygame.K_m:
                    print_debug(f"Before {game_container.health}")
                    game_container.set_health(game_container.health - 10)
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
                for mcard in sprite_group:
                    if mcard.check_mouse_up(mouse_pos):
                        click_event_player(mcard)





        # Flush the screen
        screen.fill("darkred")




        # get input
        # handle input
        # redraw
        adjust_surfaces(screen, sprite_group)
        sprite_group.draw(screen)
        # print(board_sprite_group)
        board_sprite_group.draw(screen)
        gui_sprite_group.draw(screen)
        # draw_circles(screen, spread_card(5, WIDTH))
        # draw_rects(screen, spread_card(card_count, WIDTH))
        draw_guide_lines(screen)
        pygame.display.flip()

        delta_time = clock.tick(FPS) / 1000


if __name__ == "__main__":
    Game()
