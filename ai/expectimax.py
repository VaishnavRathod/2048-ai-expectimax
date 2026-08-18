import math

from ai.evaluation import BoardEvaluator
from ai.simulator import BoardSimulator

from game.settings import BOARD_SIZE


class ExpectimaxAI:

    def __init__(self, depth=4):

        # ==========================================
        # AI SEARCH DEPTH
        # ==========================================

        self.depth = depth


        # ==========================================
        # COMPONENTS
        # ==========================================

        self.evaluator = BoardEvaluator()

        self.simulator = BoardSimulator()


    def get_move_scores(self, board):

        possible_moves = (
            self.simulator.get_possible_moves(
                board
            )
        )

        move_scores = {}

        for move, new_board in possible_moves.items():

            score = self.expectimax(
                new_board,
                self.depth - 1,
                False
            )

            move_scores[move] = score

        return move_scores


    # ==========================================
    # GET BEST MOVE
    # ==========================================

    def get_best_move(self, board):

        move_scores = self.get_move_scores(
            board
        )

        if not move_scores:

            return None

        best_move = max(
            move_scores,
            key=move_scores.get
        )

        return best_move


    # ==========================================
    # EXPECTIMAX
    # ==========================================

    def expectimax(
        self,
        board,
        depth,
        player_turn
    ):

        # ======================================
        # STOP CONDITION
        # ======================================

        if depth <= 0:

            return self.evaluator.evaluate(
                board
            )


        # ======================================
        # PLAYER TURN
        # ======================================

        if player_turn:

            return self.max_value(
                board,
                depth
            )


        # ======================================
        # RANDOM TILE TURN
        # ======================================

        else:

            return self.expectation_value(
                board,
                depth
            )


    # ==========================================
    # MAX NODE
    # ==========================================

    def max_value(
        self,
        board,
        depth
    ):

        possible_moves = (
            self.simulator.get_possible_moves(
                board
            )
        )


        # No moves

        if not possible_moves:

            return self.evaluator.evaluate(
                board
            )


        best_score = -math.inf


        # ======================================
        # TRY EVERY MOVE
        # ======================================

        for move, new_board in (
            possible_moves.items()
        ):

            score = self.expectimax(
                new_board,
                depth - 1,
                False
            )


            best_score = max(
                best_score,
                score
            )


        return best_score


    # ==========================================
    # EXPECTATION NODE
    # ==========================================

    def expectation_value(
        self,
        board,
        depth
    ):

        empty_cells = (
            self.simulator.get_empty_cells(
                board
            )
        )


        # No empty cells

        if not empty_cells:

            return self.max_value(
                board,
                depth - 1
            )


        total_score = 0.0


        # ======================================
        # RANDOM TILE PROBABILITIES
        # ======================================

        # 2 appears 90% of the time

        probability_2 = 0.9


        # 4 appears 10% of the time

        probability_4 = 0.1


        # ======================================
        # CALCULATE EXPECTED VALUE
        # ======================================

        for position in empty_cells:


            # ----------------------------------
            # Place 2
            # ----------------------------------

            board_with_2 = (
                self.simulator.add_tile(
                    board,
                    position,
                    2
                )
            )


            score_2 = self.expectimax(
                board_with_2,
                depth - 1,
                True
            )


            # ----------------------------------
            # Place 4
            # ----------------------------------

            board_with_4 = (
                self.simulator.add_tile(
                    board,
                    position,
                    4
                )
            )


            score_4 = self.expectimax(
                board_with_4,
                depth - 1,
                True
            )


            # ----------------------------------
            # Expected value
            # ----------------------------------

            expected_score = (

                probability_2 * score_2

                +

                probability_4 * score_4
            )


            total_score += (
                expected_score
            )


        # ======================================
        # Average across empty cells
        # ======================================

        return (
            total_score
            / len(empty_cells)
        )