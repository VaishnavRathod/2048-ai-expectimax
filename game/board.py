import random

from game.settings import (
    BOARD_SIZE,
    STARTING_TILES,
    FOUR_PROBABILITY
)


class Board:

    def __init__(self):

        self.grid = [
            [0 for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]

        self.add_starting_tiles()


    # ==========================================
    # STARTING TILES
    # ==========================================

    def add_starting_tiles(self):

        for _ in range(STARTING_TILES):
            self.add_random_tile()


    # ==========================================
    # EMPTY CELLS
    # ==========================================

    def get_empty_cells(self):

        empty_cells = []

        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                if self.grid[row][col] == 0:

                    empty_cells.append(
                        (row, col)
                    )

        return empty_cells


    # ==========================================
    # RANDOM TILE
    # ==========================================

    def add_random_tile(self):

        empty_cells = self.get_empty_cells()

        if not empty_cells:
            return False

        row, col = random.choice(
            empty_cells
        )

        if random.random() < FOUR_PROBABILITY:

            value = 4

        else:

            value = 2

        self.grid[row][col] = value

        return True


    # ==========================================
    # CHECK FULL
    # ==========================================

    def is_full(self):

        return len(
            self.get_empty_cells()
        ) == 0


    # ==========================================
    # COPY BOARD
    # ==========================================

    def copy(self):

        return [
            row.copy()
            for row in self.grid
        ]


    # ==========================================
    # PRINT BOARD
    # ==========================================

    def print_board(self):

        print()

        for row in self.grid:

            print(
                " | ".join(
                    str(value)
                    if value != 0
                    else "."
                    for value in row
                )
            )

        print()