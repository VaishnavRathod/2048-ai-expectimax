import copy

from game.settings import BOARD_SIZE


class BoardSimulator:

    def __init__(self):

        pass


    # ==========================================
    # COPY BOARD
    # ==========================================

    def copy_board(self, board):

        return [
            row.copy()
            for row in board
        ]


    # ==========================================
    # MOVE LEFT
    # ==========================================

    def move_left(self, board):

        new_board = self.copy_board(board)

        for row in range(BOARD_SIZE):

            new_board[row] = (
                self.process_row_left(
                    new_board[row]
                )
            )

        return new_board


    # ==========================================
    # MOVE RIGHT
    # ==========================================

    def move_right(self, board):

        new_board = self.copy_board(board)

        for row in range(BOARD_SIZE):

            reversed_row = (
                new_board[row][::-1]
            )

            moved_row = (
                self.process_row_left(
                    reversed_row
                )
            )

            new_board[row] = (
                moved_row[::-1]
            )

        return new_board


    # ==========================================
    # MOVE UP
    # ==========================================

    def move_up(self, board):

        new_board = self.copy_board(board)

        # Transpose

        new_board = self.transpose(
            new_board
        )


        # Move every row left

        for row in range(BOARD_SIZE):

            new_board[row] = (
                self.process_row_left(
                    new_board[row]
                )
            )


        # Transpose back

        new_board = self.transpose(
            new_board
        )

        return new_board


    # ==========================================
    # MOVE DOWN
    # ==========================================

    def move_down(self, board):

        new_board = self.copy_board(board)

        # Transpose

        new_board = self.transpose(
            new_board
        )


        # Reverse rows

        for row in range(BOARD_SIZE):

            new_board[row] = (
                new_board[row][::-1]
            )


        # Move left

        for row in range(BOARD_SIZE):

            new_board[row] = (
                self.process_row_left(
                    new_board[row]
                )
            )


        # Reverse again

        for row in range(BOARD_SIZE):

            new_board[row] = (
                new_board[row][::-1]
            )


        # Transpose back

        new_board = self.transpose(
            new_board
        )

        return new_board


    # ==========================================
    # PROCESS ROW
    # ==========================================

    def process_row_left(self, row):

        # Remove empty cells

        values = [
            value
            for value in row
            if value != 0
        ]


        result = []

        i = 0


        while i < len(values):

            # ----------------------------------
            # Merge
            # ----------------------------------

            if (
                i + 1 < len(values)
                and values[i]
                == values[i + 1]
            ):

                result.append(
                    values[i] * 2
                )

                i += 2


            # ----------------------------------
            # Normal tile
            # ----------------------------------

            else:

                result.append(
                    values[i]
                )

                i += 1


        # Fill empty spaces

        while len(result) < BOARD_SIZE:

            result.append(0)


        return result


    # ==========================================
    # TRANSPOSE
    # ==========================================

    def transpose(self, board):

        return [
            list(column)
            for column in zip(*board)
        ]


    # ==========================================
    # GET POSSIBLE MOVES
    # ==========================================

    def get_possible_moves(self, board):

        possible_moves = {}


        # --------------------------------------
        # LEFT
        # --------------------------------------

        left = self.move_left(board)

        if left != board:

            possible_moves["left"] = left


        # --------------------------------------
        # RIGHT
        # --------------------------------------

        right = self.move_right(board)

        if right != board:

            possible_moves["right"] = right


        # --------------------------------------
        # UP
        # --------------------------------------

        up = self.move_up(board)

        if up != board:

            possible_moves["up"] = up


        # --------------------------------------
        # DOWN
        # --------------------------------------

        down = self.move_down(board)

        if down != board:

            possible_moves["down"] = down


        return possible_moves


    # ==========================================
    # EMPTY CELLS
    # ==========================================

    def get_empty_cells(self, board):

        empty_cells = []


        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                if board[row][col] == 0:

                    empty_cells.append(
                        (row, col)
                    )


        return empty_cells


    # ==========================================
    # ADD TILE
    # ==========================================

    def add_tile(
        self,
        board,
        position,
        value
    ):

        new_board = self.copy_board(
            board
        )

        row, col = position

        new_board[row][col] = value

        return new_board