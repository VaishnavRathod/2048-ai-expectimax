import math

from game.settings import BOARD_SIZE


class BoardEvaluator:

    def __init__(self):

        # ======================================
        # HEURISTIC WEIGHTS
        # ======================================

        self.empty_weight = 2.7

        self.monotonicity_weight = 1.5

        self.smoothness_weight = 0.8

        self.max_tile_weight = 1.0

        self.corner_weight = 2.0


    # ==========================================
    # MAIN EVALUATION FUNCTION
    # ==========================================

    def evaluate(self, board):

        empty_score = (
            self.evaluate_empty_cells(board)
        )

        monotonicity_score = (
            self.evaluate_monotonicity(board)
        )

        smoothness_score = (
            self.evaluate_smoothness(board)
        )

        max_tile_score = (
            self.evaluate_max_tile(board)
        )

        corner_score = (
            self.evaluate_corner(board)
        )


        total_score = (

            self.empty_weight
            * empty_score

            +

            self.monotonicity_weight
            * monotonicity_score

            +

            self.smoothness_weight
            * smoothness_score

            +

            self.max_tile_weight
            * max_tile_score

            +

            self.corner_weight
            * corner_score
        )


        return total_score


    # ==========================================
    # EMPTY CELLS
    # ==========================================

    def evaluate_empty_cells(self, board):

        empty_cells = 0

        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                if board[row][col] == 0:

                    empty_cells += 1


        return empty_cells


    # ==========================================
    # MONOTONICITY
    # ==========================================

    def evaluate_monotonicity(self, board):

        score = 0


        # --------------------------------------
        # Rows
        # --------------------------------------

        for row in range(BOARD_SIZE):

            increasing = 0

            decreasing = 0

            for col in range(
                BOARD_SIZE - 1
            ):

                current = board[row][col]

                next_value = (
                    board[row][col + 1]
                )


                if current == 0:
                    continue

                if next_value == 0:
                    continue


                current_log = math.log2(
                    current
                )

                next_log = math.log2(
                    next_value
                )


                difference = (
                    next_log
                    - current_log
                )


                if difference > 0:

                    increasing += difference

                elif difference < 0:

                    decreasing -= difference


            score += max(
                increasing,
                decreasing
            )


        # --------------------------------------
        # Columns
        # --------------------------------------

        for col in range(BOARD_SIZE):

            increasing = 0

            decreasing = 0

            for row in range(
                BOARD_SIZE - 1
            ):

                current = board[row][col]

                next_value = (
                    board[row + 1][col]
                )


                if current == 0:
                    continue

                if next_value == 0:
                    continue


                current_log = math.log2(
                    current
                )

                next_log = math.log2(
                    next_value
                )


                difference = (
                    next_log
                    - current_log
                )


                if difference > 0:

                    increasing += difference

                elif difference < 0:

                    decreasing -= difference


            score += max(
                increasing,
                decreasing
            )


        return score


    # ==========================================
    # SMOOTHNESS
    # ==========================================

    def evaluate_smoothness(self, board):

        score = 0


        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                current = board[row][col]

                if current == 0:

                    continue


                current_log = math.log2(
                    current
                )


                # Right neighbor

                if col + 1 < BOARD_SIZE:

                    right = (
                        board[row][col + 1]
                    )

                    if right != 0:

                        right_log = math.log2(
                            right
                        )

                        score -= abs(
                            current_log
                            - right_log
                        )


                # Bottom neighbor

                if row + 1 < BOARD_SIZE:

                    bottom = (
                        board[row + 1][col]
                    )

                    if bottom != 0:

                        bottom_log = math.log2(
                            bottom
                        )

                        score -= abs(
                            current_log
                            - bottom_log
                        )


        return score


    # ==========================================
    # MAXIMUM TILE
    # ==========================================

    def evaluate_max_tile(self, board):

        max_tile = 0

        for row in board:

            for value in row:

                if value > max_tile:

                    max_tile = value


        if max_tile == 0:

            return 0


        return math.log2(
            max_tile
        )


    # ==========================================
    # CORNER BONUS
    # ==========================================

    def evaluate_corner(self, board):

        max_tile = 0

        for row in board:

            for value in row:

                max_tile = max(
                    max_tile,
                    value
                )


        if max_tile == 0:

            return 0


        corners = [

            board[0][0],

            board[0][BOARD_SIZE - 1],

            board[BOARD_SIZE - 1][0],

            board[BOARD_SIZE - 1][
                BOARD_SIZE - 1
            ]
        ]


        if max_tile in corners:

            return math.log2(
                max_tile
            )

        return 0