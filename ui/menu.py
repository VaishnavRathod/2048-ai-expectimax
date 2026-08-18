import pygame

from ui.colors import (
    BACKGROUND_COLOR,
    DARK_TEXT
)


class Menu:

    def __init__(self, screen):

        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        self.title_font = pygame.font.Font(
            None,
            70
        )

        self.button_font = pygame.font.Font(
            None,
            35
        )


    # ==========================================
    # DRAW START MENU
    # ==========================================

    def draw_start_menu(self):

        self.screen.fill(
            BACKGROUND_COLOR
        )

        # Title

        title = self.title_font.render(
            "2048",
            True,
            DARK_TEXT
        )

        title_rect = title.get_rect()

        title_rect.center = (
            self.width // 2,
            self.height // 3
        )

        self.screen.blit(
            title,
            title_rect
        )


        # Start text

        start_text = self.button_font.render(
            "Press ENTER to Start",
            True,
            DARK_TEXT
        )

        start_rect = start_text.get_rect()

        start_rect.center = (
            self.width // 2,
            self.height // 2
        )

        self.screen.blit(
            start_text,
            start_rect
        )