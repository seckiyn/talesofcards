""" PyGame related tools"""
from typing import Tuple, Iterable
import pygame
from config import WIDTH, HEIGHT
from gameobjects import Card

pygame.init()  # pylint: disable=no-member


def draw_line(surface, cord1, cord2, width=3, color="purple"):
    """
        Draw lines for debug
    """
    pygame.draw.line(surface, color, cord1, cord2, width)


def draw_guide_lines(surface):
    """
        Draw guide lines for geometry
    """
    half_width: int = WIDTH // 2
    third_height: int = HEIGHT // 3

    # Board-Top Horizontal line
    # cord1_x = 0
    # cord1_y = third_height
    # cord2_x = WIDTH
    # cord2_y = cord1_y
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    draw_line(surface, (0, third_height), (WIDTH, third_height))

    # Board-Bottom Horizontal line
    # cord1_x = 0
    # cord1_y = 2 * third_height
    # cord2_x = WIDTH
    # cord2_y = cord1_y
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    draw_line(surface, (0, 2 * third_height), (WIDTH, 2 * third_height))

    # Opponent Card Guide Line
    # cord1_x = 0
    # cord1_y = third_height // 2
    # cord2_x = WIDTH
    # cord2_y = cord1_y
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    draw_line(surface, (0, third_height//2), (WIDTH, third_height//2), 1)

    # Board Card Guide Line also horizontal center
    # cord1_x = 0
    # cord1_y = 3 * (third_height // 2)
    # cord2_x = WIDTH
    # cord2_y = cord1_y
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    bcgl_y = 3*(third_height//2)
    draw_line(surface, (0, bcgl_y), (WIDTH, bcgl_y), 1, "green")

    # Player Card Guide Line
    # cord1_x = 0
    # cord1_y = 5 * (third_height // 2)
    # cord2_x = WIDTH
    # cord2_y = cord1_y
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    pcgl_y = 5*(third_height//2)
    draw_line(surface, (0, pcgl_y), (WIDTH, pcgl_y), 1)

    # Center Vertical line
    # cord1_x = half_width
    # cord1_y = 0
    # cord2_x = cord1_x
    # cord2_y = HEIGHT
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    draw_line(surface, (half_width, 0), (half_width, HEIGHT), 1, "green")

    # Left Vertical line
    # cord1_x = half_width // 2
    # cord1_y = 0
    # cord2_x = cord1_x
    # cord2_y = HEIGHT
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    draw_line(surface, (half_width//2, 0), (half_width//2, HEIGHT), 1, "green")

    # Right Vertical line
    # cord1_x = 3 * (half_width // 2)
    # cord1_y = 0
    # cord2_x = cord1_x
    # cord2_y = HEIGHT
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    rvl_x = 3 * (half_width//2)

    draw_line(surface, (rvl_x, 0), (rvl_x, HEIGHT), 1, "green")

    # LeftSide-Left Vertical line
    # cord1_x = (half_width // 2) // 2
    # cord1_y = 0
    # cord2_x = cord1_x
    # cord2_y = HEIGHT
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    llvl_x = (half_width//2)//2
    draw_line(surface, (llvl_x, 0), (llvl_x, HEIGHT), 1, "lightblue")

    # Board-Bottom Horizontal line - Board Guide Line
    # cord1_x = 0
    # cord1_y = 7 * (third_height // 4)
    # cord2_x = WIDTH
    # cord2_y = cord1_y
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    bbot_y = 7 * (third_height // 4)
    draw_line(surface, (0, bbot_y), (WIDTH, bbot_y), 1, color="lightblue")

    # Board-TOP Horizontal line - Board Guide Line
    # cord1_x = 0
    # cord1_y = 5 * (third_height // 4)
    # cord2_x = WIDTH
    # cord2_y = cord1_y
    # cord1 = cord1_x, cord1_y
    # cord2 = cord2_x, cord2_y
    btop_y = 5 * (third_height // 4)
    draw_line(surface, (0, btop_y), (WIDTH, btop_y), 1, color="lightblue")


def spread_card(
        card_count: int,
        size: float,
        cardsize=157,
        padding=10) -> Tuple[int, ...]:
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


def adjust_surfaces(surf: Iterable[Card]) -> None:
    """
        Takes the tuple of surfaces(surf) and adjusts them according to
        x values given by spread_card function
    """
    if not surf:
        return
    x_cords = spread_card(len(surf), WIDTH)
    for x_cord, card in zip(x_cords, surf):
        card.rect.center = x_cord, 5 * (HEIGHT // 6)
