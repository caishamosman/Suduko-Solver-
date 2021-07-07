""" A simple Suduko Game
"""

import requests
import pygame

# Initialize pygame
pygame.init()

# Set constant variables
WIDTH, HEIGHT = 642, 642
WHITE, BLACK, GREEN = (255, 255, 255), (0, 0, 0), (152, 251, 152)
TPS = 60
BARRIER = 5

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Suduko Game")
FONT = pygame.font.SysFont("calibri", 35)

# Get an external valid Suduko populator
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=random")
grid = response.json()["board"]
ORIGINAL_GRID = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]


def main():

    """
    Play a Suduko Game
    """

    timer = pygame.time.Clock()

    running = True
    while running:
        # Ensure a constant number of runs per 60s
        timer.tick(TPS)

        for event in pygame.event.get():

            # User closes window screen
            if event.type == pygame.QUIT:
                running = False

            # User clicks on a cell in the Suduko game
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

                insert_value(SCREEN, ((pos[0]+68)//68, (pos[1]+68)//68))

        # Draw the window
        draw_window()
        # Populate the grid
        populate_grid()

    # Quit Game
    pygame.quit()


def draw_window():
    """
    Draw a window that contains a 9x9 grid with 3×3 subgrids

    :return: a 9x9 grid with 3×3 subgrids
    :rtype:Surface
    """
    # Make background colour green
    SCREEN.fill(GREEN)

    pygame.draw.rect(SCREEN, WHITE, pygame.Rect(15, 15, 612, 612), 5)

    for i in range(68, 612, 68):

        # Set up thick vs thin lines
        line_width = 2 if i % 3 != 0 else 5

        # Set up the horizontal lines
        pygame.draw.line(SCREEN, WHITE, pygame.Vector2((i+15, 15)), pygame.Vector2(i+15, 627), line_width)

        # Set up the vertical lines
        pygame.draw.line(SCREEN, WHITE, pygame.Vector2((15, i+15)), pygame.Vector2(627, i+15), line_width)

    pygame.display.update()


def populate_grid():
    """
     Populate the grid with a partially completed Sudoku grid

     :return: A partially completed Sudoku grid
     :rtype: Surface
     """

    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if 0 < grid[i][j] < 10:

                # Copy int value and put it on the screen window
                interger = FONT.render(str(grid[i][j]), True, BLACK)
                SCREEN.blit(interger, ((j+1)*68 - 28, (i+1)*68 - 35))

    pygame.display.update()


def insert_value(window, position):

    """
    Insert a number into an available Suduko position

    :param window: A pygame window
    :type window: Surface
    :param position: position of the click
    :type position: tuple
    :return: a window with updated values
    :rtype: Surface
    """
    x, y = position[1], position[0]
    run = True

    while run:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            # When a value is entered on the keyboard
            if event.type == pygame.KEYDOWN:

                # Don't allow changes to pre-set values
                if ORIGINAL_GRID[x-1][y-1] == 0:
                    run = False

                # clearing non pre-set values to zero
                if event.key == 48:
                    grid[x-1][y-1] = event.key - 48
                    pygame.draw.rect(window, GREEN, (position[0]*68+BARRIER, position[1]*68+BARRIER,
                                                     68 - 2*BARRIER, 68 - 2*BARRIER))
                    pygame.display.update()

                # Setting clearing non pre-set values to zero to valid numbers
                if 0 < event.key-48 < 10:
                    grid[x-1][y-1] = event.key-48
                    # Draw new rectangle to cover previous value
                    pygame.draw.rect(window, GREEN, (position[0] * 68 + BARRIER, position[1] * 68 + BARRIER,
                                                     68 - 2 * BARRIER, 68 - 2 * BARRIER))

                    ascii_int = event.key - 48
                    value = FONT.render(str(ascii_int), True, BLACK)
                    window.blit(value, ((position[0])*68-68, (position[1])*68-68))

                    pygame.display.update()


if __name__ == "__main__":
    main()
