import pygame
from typing import Tuple
from pygame import Rect

pygame.init()
"""
self.width = 1500
self.height = 750
"""

# Screen Setup
WIDTH: int = 1500
HEIGHT: int = 750
WINDOW_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)
FPS = 60


class Sprite(pygame.sprite.Sprite):
    def __init__(self, imagepath: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()


def draw_line(surface, cord1, cord2, width=3, color="purple"):
    pygame.draw.line(surface, color, cord1, cord2, width)


def draw_guide_lines(surface):
    HALFWIDTH:int  = WIDTH // 2
    THIRDHEIGHT:int = HEIGHT // 3
    # Board line
    cord1_x = 0
    cord1_y = THIRDHEIGHT
    cord2_x = WIDTH
    cord2_y = cord1_y 
    cord1 = cord1_x, cord1_y
    cord2 = cord2_x, cord2_y
    draw_line(surface, cord1, cord2)

    # Board line
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


def spread_card(card_count: int, size: float, cardsize=157, padding=10) -> Tuple[int, ...]:
    """
    -----------------------
    """
    halfsize = size // 2
    halfpadding = padding // 2
    halfcardsize = cardsize // 2

    if card_count <= 0 or not isinstance(card_count, int):
        raise ValueError("Card count must be a positive integer")

    if card_count > 8:
        card_count = 8
    if card_count == 1:
        return size // 2,
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
"""
    if card_count == 4:
        left, right = spread_card(2, size)
        mostleft = left - padding - cardsize
        mostright = right + padding + cardsize
        return mostleft, left, right, mostright
    if card_count == 5:
        left, middle, right = spread_card(3, size)
        mostleft = left - padding - cardsize
        mostright = right + padding + cardsize
        return mostleft, left, middle, right, mostright
    if card_count == 6:
        left, *middle, right = spread_card(4, size)
        mostleft = left - padding - cardsize
        mostright = right + padding + cardsize
        return (mostleft, left, *middle, right, mostright)
    if card_count == 7:
        left, *middle, right = spread_card(5, size)
        mostleft = left - padding - cardsize
        mostright = right + padding + cardsize
        return (mostleft, left, *middle, right, mostright)
    if card_count == 8:
        left, *middle, right = spread_card(5, size)
        mostleft = left - padding - cardsize
        mostright = right + padding + cardsize
        return (mostleft, left, *middle, right, mostright)
"""

def draw_circles(surface, x_cords: Tuple[int, ...]) -> None:
    for x_cord in x_cords:
        pygame.draw.circle(surface, "red", (x_cord, 5 * (HEIGHT // 6)), 157)


def draw_rects(surface, x_cords: Tuple[int, ...]) -> None:
    for x_cord in x_cords:
        width = 157
        height = 250
        rect = pygame.Rect(0, 0, width, height)
        rect.center = x_cord, 5 * (HEIGHT // 6)
        pygame.draw.rect(surface, "red", rect)



def Game() -> None:
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    running = True
    delta_time = 0
    sprite_group = pygame.sprite.Group()
    card = Sprite("./cards/card.png")
    card2 = Sprite("./cards/card2.png")
    card2.rect.center = WIDTH // 2, HEIGHT // 2
    sprite_group.add((card, card2))
    card_count = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_k:
                    card_count += 1


        # Flush the screen
        screen.fill("darkred")
        sprite_group.draw(screen)
        # draw_circles(screen, spread_card(5, WIDTH))
        draw_rects(screen, spread_card(card_count, WIDTH))


        # get input
        # handle input
        # redraw
        draw_guide_lines(screen)
        pygame.display.flip()

        delta_time = clock.tick(FPS) / 1000


if __name__ == "__main__":
    Game()
