import pygame

from game.board import Board
from game.game_logic import GameLogic

from game.settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    WINDOW_TITLE
)

from ui.renderer import Renderer
from ai.expectimax import ExpectimaxAI


# ==========================================
# PERFORM MOVE
# ==========================================

def perform_move(
    game,
    renderer,
    ai,
    direction
):

    if direction == "left":

        changed, old_board, new_board = (
            game.move_left()
        )

    elif direction == "right":

        changed, old_board, new_board = (
            game.move_right()
        )

    elif direction == "up":

        changed, old_board, new_board = (
            game.move_up()
        )

    elif direction == "down":

        changed, old_board, new_board = (
            game.move_down()
        )

    else:

        return


    if changed:

        # ==================================
        # PLAY ANIMATION
        # ==================================

        renderer.animate_move(
            old_board,
            new_board,
            direction,
            game.score
        )


        # ==================================
        # ADD RANDOM TILE
        # ==================================

        game.add_random_tile()


        # ==================================
        # CHECK GAME
        # ==================================

        game.check_win()

        game.check_game_over()


        # ==================================
        # CALCULATE NEW AI SUGGESTION
        # ==================================

        update_ai_suggestion(
            game,
            ai,
            renderer
        )


def update_ai_suggestion(
    game,
    ai,
    renderer
):

    if game.game_over:

        renderer.set_ai_analysis(
            None,
            {}
        )

        return


    if game.won:

        renderer.set_ai_analysis(
            None,
            {}
        )

        return


    # ======================================
    # GET SCORES
    # ======================================

    move_scores = ai.get_move_scores(
        game.board.grid
    )


    # ======================================
    # NO MOVES
    # ======================================

    if not move_scores:

        renderer.set_ai_analysis(
            None,
            {}
        )

        return


    # ======================================
    # BEST MOVE
    # ======================================

    best_move = max(
        move_scores,
        key=move_scores.get
    )


    # ======================================
    # SEND TO RENDERER
    # ======================================

    renderer.set_ai_analysis(
        best_move,
        move_scores
    )

# ==========================================
# MAIN
# ==========================================

def main():

    pygame.init()


    # ======================================
    # WINDOW
    # ======================================

    screen = pygame.display.set_mode(
        (
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )
    )

    pygame.display.set_caption(
        WINDOW_TITLE
    )


    clock = pygame.time.Clock()


    # ======================================
    # CREATE GAME
    # ======================================

    board = Board()

    game = GameLogic(
        board
    )

    renderer = Renderer(
        screen
    )

    ai = ExpectimaxAI(
        depth=2
    )

    update_ai_suggestion(
        game,
        ai,
        renderer
    )

    # ======================================
    # MAIN LOOP
    # ======================================

    running = True

    while running:


        # ==================================
        # EVENTS
        # ==================================

        for event in pygame.event.get():


            # --------------------------------
            # QUIT
            # --------------------------------

            if event.type == pygame.QUIT:

                running = False


            # --------------------------------
            # KEYBOARD
            # --------------------------------

            elif event.type == pygame.KEYDOWN:


                # Don't move after game over

                if game.game_over:

                    continue


                # Don't move after winning

                if game.won:

                    continue


                # --------------------------------
                # LEFT
                # --------------------------------

                if event.key == pygame.K_LEFT:

                    perform_move(
                        game,
                        renderer,
                        ai,
                        "left"
                    )


                elif event.key == pygame.K_RIGHT:

                    perform_move(
                        game,
                        renderer,
                        ai,
                        "right"
                    )


                elif event.key == pygame.K_UP:

                    perform_move(
                        game,
                        renderer,
                        ai,
                        "up"
                    )


                elif event.key == pygame.K_DOWN:

                    perform_move(
                        game,
                        renderer,
                        ai,
                        "down"
                    )


        # ==================================
        # DRAW
        # ==================================

        renderer.draw(
            game
        )


        # ==================================
        # DISPLAY
        # ==================================

        pygame.display.flip()


        # ==================================
        # FPS
        # ==================================

        clock.tick(
            FPS
        )


    # ======================================
    # QUIT
    # ======================================

    pygame.quit()


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()