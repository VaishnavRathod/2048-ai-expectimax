from game.settings import (
    BOARD_SIZE,
    WINNING_TILE
)


class GameLogic:

    def __init__(self, board):

        self.board = board

        self.score = 0

        self.won = False

        self.game_over = False


    # ==========================================
    # MOVE ROW LEFT
    # ==========================================

    def move_row_left(self, row):

        # Remove zeros
        row = [
            value
            for value in row
            if value != 0
        ]

        merged = []

        i = 0

        while i < len(row):

            if (
                i + 1 < len(row)
                and row[i] == row[i + 1]
            ):

                new_value = row[i] * 2

                merged.append(new_value)

                self.score += new_value

                i += 2

            else:

                merged.append(
                    row[i]
                )

                i += 1


        # Fill remaining spaces

        while len(merged) < BOARD_SIZE:

            merged.append(0)

        return merged


    # ==========================================
    # MOVE LEFT
    # ==========================================

    def move_left(self):

        old_board = self.board.copy()

        for row in range(BOARD_SIZE):

            self.board.grid[row] = (
                self.move_row_left(
                    self.board.grid[row]
                )
            )

        return self.finish_move(
            old_board
        )


    # ==========================================
    # MOVE RIGHT
    # ==========================================

    def move_right(self):

        old_board = self.board.copy()

        for row in range(BOARD_SIZE):

            reversed_row = (
                self.board.grid[row][::-1]
            )

            moved_row = (
                self.move_row_left(
                    reversed_row
                )
            )

            self.board.grid[row] = (
                moved_row[::-1]
            )

        return self.finish_move(
            old_board
        )


    # ==========================================
    # TRANSPOSE
    # ==========================================

    def transpose(self):

        self.board.grid = [
            list(column)
            for column in zip(
                *self.board.grid
            )
        ]


    # ==========================================
    # MOVE UP
    # ==========================================

    def move_up(self):

        old_board = self.board.copy()

        self.transpose()

        for row in range(BOARD_SIZE):

            self.board.grid[row] = (
                self.move_row_left(
                    self.board.grid[row]
                )
            )

        self.transpose()

        return self.finish_move(
            old_board
        )


    # ==========================================
    # MOVE DOWN
    # ==========================================

    def move_down(self):

        old_board = self.board.copy()

        self.transpose()

        for row in range(BOARD_SIZE):

            self.board.grid[row] = (
                self.board.grid[row][::-1]
            )

        for row in range(BOARD_SIZE):

            self.board.grid[row] = (
                self.move_row_left(
                    self.board.grid[row]
                )
            )

        for row in range(BOARD_SIZE):

            self.board.grid[row] = (
                self.board.grid[row][::-1]
            )

        self.transpose()

        return self.finish_move(
            old_board
        )


    # ==========================================
    # FINISH MOVE
    # ==========================================

    def finish_move(self, old_board):

        changed = (
            old_board != self.board.grid
        )

        if not changed:

            return (
                False,
                old_board,
                old_board
            )


        # Save resulting board
        new_board = self.board.copy()


        # Check win
        self.check_win()


        # We don't add the random tile here.
        #
        # It will be added AFTER the animation.

        return (
            True,
            old_board,
            new_board
        )


    # ==========================================
    # ADD RANDOM TILE
    # ==========================================

    def add_random_tile(self):

        return self.board.add_random_tile()


    # ==========================================
    # CHECK WIN
    # ==========================================

    def check_win(self):

        for row in self.board.grid:

            for value in row:

                if value >= WINNING_TILE:

                    self.won = True

                    return True

        return False


    # ==========================================
    # CHECK GAME OVER
    # ==========================================

    def check_game_over(self):

        # Empty cell means moves are still possible

        if not self.board.is_full():

            self.game_over = False

            return False


        # Check horizontal matches

        for row in range(BOARD_SIZE):

            for col in range(
                BOARD_SIZE - 1
            ):

                if (
                    self.board.grid[row][col]
                    ==
                    self.board.grid[row][col + 1]
                ):

                    self.game_over = False

                    return False


        # Check vertical matches

        for row in range(
            BOARD_SIZE - 1
        ):

            for col in range(BOARD_SIZE):

                if (
                    self.board.grid[row][col]
                    ==
                    self.board.grid[row + 1][col]
                ):

                    self.game_over = False

                    return False


        self.game_over = True

        return True