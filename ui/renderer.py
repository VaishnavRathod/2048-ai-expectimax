import pygame

from game.settings import (
    BOARD_SIZE,
    ANIMATION_DURATION
)

from ui.colors import (
    BACKGROUND_COLOR,
    BOARD_COLOR,
    EMPTY_TILE_COLOR,
    TILE_COLORS,
    DARK_TEXT,
    LIGHT_TEXT,
    SCORE_TEXT,
    TITLE_TEXT
)


class Renderer:

    def __init__(self, screen):

        self.screen = screen

        self.width = (
            screen.get_width()
        )

        self.height = (
            screen.get_height()
        )

        self.ai_move_scores = {}


        # ======================================
        # BOARD
        # ======================================

        self.board_size = 500

        self.tile_size = (
            self.board_size
            // BOARD_SIZE
        )

        self.board_x = 40

        self.board_y = 150


        # ======================================
        # FONTS
        # ======================================

        self.title_font = pygame.font.Font(
            None,
            60
        )

        self.tile_font = pygame.font.Font(
            None,
            36
        )

        self.score_font = pygame.font.Font(
            None,
            28
        )

        self.message_font = pygame.font.Font(
            None,
            45
        )

        # ==========================================
        # AI SUGGESTION
        # ==========================================

        self.ai_suggestion = None

        self.ai_thinking = False

        self.ai_font = pygame.font.Font(
            None,
            24
        )

        self.ai_title_font = pygame.font.Font(
            None,
            26
        )


    # ==========================================
    # DRAW GAME
    # ==========================================

    def draw(self, game):

        self.screen.fill(
            BACKGROUND_COLOR
        )

        self.draw_title()

        self.draw_score(
            game.score
        )

        self.draw_board(
            game.board.grid
        )

        self.draw_ai_suggestion()


        if game.won:

            self.draw_message(
                "You reached 2048!"
            )

        elif game.game_over:

            self.draw_message(
                "Game Over!"
            )


    # ==========================================
    # TITLE
    # ==========================================

    def draw_title(self):

        title = self.title_font.render(
            "2048",
            True,
            TITLE_TEXT
        )

        rect = title.get_rect()

        rect.centerx = (
            self.width // 2
        )

        rect.y = 30

        self.screen.blit(
            title,
            rect
        )


    # ==========================================
    # SCORE
    # ==========================================

    def draw_score(self, score):

        text = self.score_font.render(
            f"Score: {score}",
            True,
            SCORE_TEXT
        )

        rect = text.get_rect()

        rect.centerx = (
            self.width // 2
        )

        rect.y = 100

        self.screen.blit(
            text,
            rect
        )


    # ==========================================
    # BOARD
    # ==========================================

    def draw_board(self, grid):

        pygame.draw.rect(
            self.screen,
            BOARD_COLOR,
            (
                self.board_x,
                self.board_y,
                self.board_size,
                self.board_size
            ),
            border_radius=10
        )


        for row in range(
            BOARD_SIZE
        ):

            for col in range(
                BOARD_SIZE
            ):

                value = grid[row][col]

                self.draw_tile(
                    value,
                    row,
                    col
                )


    # ==========================================
    # TILE
    # ==========================================

    def draw_tile(
        self,
        value,
        row,
        col
    ):

        self.draw_tile_at_position(
            value,
            row,
            col
        )


    # ==========================================
    # TILE AT POSITION
    # ==========================================

    def draw_tile_at_position(
        self,
        value,
        row,
        col
    ):

        padding = 8

        x = (
            self.board_x
            + col * self.tile_size
            + padding
        )

        y = (
            self.board_y
            + row * self.tile_size
            + padding
        )

        size = (
            self.tile_size
            - 2 * padding
        )


        # Empty tile

        if value == 0:

            color = EMPTY_TILE_COLOR

        else:

            color = TILE_COLORS.get(
                value,
                TILE_COLORS[2048]
            )


        pygame.draw.rect(
            self.screen,
            color,
            (
                int(x),
                int(y),
                size,
                size
            ),
            border_radius=8
        )


        # Number

        if value != 0:

            text_color = (
                DARK_TEXT
                if value <= 4
                else LIGHT_TEXT
            )

            text = self.tile_font.render(
                str(value),
                True,
                text_color
            )

            rect = text.get_rect()

            rect.center = (
                int(x + size / 2),
                int(y + size / 2)
            )

            self.screen.blit(
                text,
                rect
            )


    # ==========================================
    # ANIMATION
    # ==========================================

    def animate_move(
        self,
        old_board,
        new_board,
        direction,
        score
    ):

        clock = pygame.time.Clock()

        start_time = (
            pygame.time.get_ticks()
        )


        while True:

            current_time = (
                pygame.time.get_ticks()
            )

            elapsed = (
                current_time
                - start_time
            )


            progress = (
                elapsed
                / ANIMATION_DURATION
            )


            if progress >= 1:

                progress = 1


            # ----------------------------------
            # Draw animation frame
            # ----------------------------------

            self.screen.fill(
                BACKGROUND_COLOR
            )

            self.draw_title()

            self.draw_score(
                score
            )

            self.draw_board_background()


            # Draw moving tiles

            self.draw_moving_tiles(
                old_board,
                new_board,
                direction,
                progress
            )


            pygame.display.flip()


            if progress >= 1:

                break


            clock.tick(60)


    # ==========================================
    # BOARD BACKGROUND
    # ==========================================

    def draw_board_background(self):

        pygame.draw.rect(
            self.screen,
            BOARD_COLOR,
            (
                self.board_x,
                self.board_y,
                self.board_size,
                self.board_size
            ),
            border_radius=10
        )


        # Empty cells

        for row in range(
            BOARD_SIZE
        ):

            for col in range(
                BOARD_SIZE
            ):

                padding = 8

                x = (
                    self.board_x
                    + col * self.tile_size
                    + padding
                )

                y = (
                    self.board_y
                    + row * self.tile_size
                    + padding
                )

                size = (
                    self.tile_size
                    - 2 * padding
                )

                pygame.draw.rect(
                    self.screen,
                    EMPTY_TILE_COLOR,
                    (
                        x,
                        y,
                        size,
                        size
                    ),
                    border_radius=8
                )


    # ==========================================
    # DRAW MOVING TILES
    # ==========================================

    def draw_moving_tiles(
        self,
        old_board,
        new_board,
        direction,
        progress
    ):

        for row in range(
            BOARD_SIZE
        ):

            for col in range(
                BOARD_SIZE
            ):

                value = (
                    old_board[row][col]
                )

                if value == 0:

                    continue


                # Determine destination

                destination = (
                    self.find_destination(
                        old_board,
                        new_board,
                        row,
                        col,
                        direction
                    )
                )


                if destination is None:

                    continue


                new_row, new_col = (
                    destination
                )


                # Interpolate position

                current_row = (
                    row
                    + (
                        new_row - row
                    ) * progress
                )

                current_col = (
                    col
                    + (
                        new_col - col
                    ) * progress
                )


                self.draw_tile_at_position(
                    value,
                    current_row,
                    current_col
                )


    # ==========================================
    # FIND DESTINATION
    # ==========================================

    def find_destination(
        self,
        old_board,
        new_board,
        row,
        col,
        direction
    ):

        value = old_board[row][col]

        if value == 0:

            return None


        # --------------------------------------
        # LEFT
        # --------------------------------------

        if direction == "left":

            target_col = col

            while (
                target_col > 0
            ):

                if (
                    new_board[row][
                        target_col - 1
                    ] != 0
                ):

                    break

                target_col -= 1

            return (
                row,
                target_col
            )


        # --------------------------------------
        # RIGHT
        # --------------------------------------

        if direction == "right":

            target_col = col

            while (
                target_col
                < BOARD_SIZE - 1
            ):

                if (
                    new_board[row][
                        target_col + 1
                    ] != 0
                ):

                    break

                target_col += 1

            return (
                row,
                target_col
            )


        # --------------------------------------
        # UP
        # --------------------------------------

        if direction == "up":

            target_row = row

            while (
                target_row > 0
            ):

                if (
                    new_board[
                        target_row - 1
                    ][col] != 0
                ):

                    break

                target_row -= 1

            return (
                target_row,
                col
            )


        # --------------------------------------
        # DOWN
        # --------------------------------------

        if direction == "down":

            target_row = row

            while (
                target_row
                < BOARD_SIZE - 1
            ):

                if (
                    new_board[
                        target_row + 1
                    ][col] != 0
                ):

                    break

                target_row += 1

            return (
                target_row,
                col
            )


        return None


    # ==========================================
    # MESSAGE
    # ==========================================

    def draw_message(
        self,
        message
    ):

        overlay = pygame.Surface(
            (
                self.board_size,
                self.board_size
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (255, 255, 255, 180)
        )

        self.screen.blit(
            overlay,
            (
                self.board_x,
                self.board_y
            )
        )


        text = self.message_font.render(
            message,
            True,
            DARK_TEXT
        )

        rect = text.get_rect()

        rect.center = (
            self.board_x
            + self.board_size // 2,

            self.board_y
            + self.board_size // 2
        )

        self.screen.blit(
            text,
            rect
        )

    def set_ai_suggestion(self, move):

        self.ai_suggestion = move


    def set_ai_analysis(
    self,
    best_move,
    move_scores
    ):

        self.ai_suggestion = best_move

        self.ai_move_scores = move_scores


    def draw_ai_suggestion(self):

    # ======================================
    # PANEL SIZE
    # ======================================

        box_width = 300
        box_height = 300


        # ======================================
        # PANEL POSITION
        # ======================================

        box_x = self.width - box_width - 30

        box_y = 170


        # ======================================
        # PANEL BACKGROUND
        # ======================================

        pygame.draw.rect(
            self.screen,
            (225, 220, 210),
            (
                box_x,
                box_y,
                box_width,
                box_height
            ),
            border_radius=12
        )


        # ======================================
        # TITLE
        # ======================================

        title = self.ai_title_font.render(
            "AI RECOMMENDS",
            True,
            DARK_TEXT
        )

        self.screen.blit(
            title,
            (
                box_x + 20,
                box_y + 20
            )
        )


        # ======================================
        # NO SUGGESTION
        # ======================================

        if self.ai_suggestion is None:

            text = self.ai_font.render(
                "No move available",
                True,
                DARK_TEXT
            )

            self.screen.blit(
                text,
                (
                    box_x + 20,
                    box_y + 65
                )
            )

            return


        # ======================================
        # ARROWS
        # ======================================

        arrows = {

            "left": "←",

            "right": "→",

            "up": "↑",

            "down": "↓"
        }


        arrow = arrows[
            self.ai_suggestion
        ]


        # ======================================
        # BEST MOVE
        # ======================================

        best_text = (
            f"{arrow}  "
            f"{self.ai_suggestion.upper()}"
        )


        rendered = self.ai_font.render(
            best_text,
            True,
            DARK_TEXT
        )


        self.screen.blit(
            rendered,
            (
                box_x + 20,
                box_y + 65
            )
        )


        # ======================================
        # MOVE SCORES
        # ======================================

        y = box_y + 115


        moves = [
            "left",
            "right",
            "up",
            "down"
        ]


        for move in moves:

            if move not in self.ai_move_scores:

                continue


            score = (
                self.ai_move_scores[move]
            )


            score_text = (
                f"{move.upper():<6} "
                f"{score:.1f}"
            )


            rendered = self.ai_font.render(
                score_text,
                True,
                DARK_TEXT
            )


            self.screen.blit(
                rendered,
                (
                    box_x + 20,
                    y
                )
            )


            y += 30