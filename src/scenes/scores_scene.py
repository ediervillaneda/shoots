import pygame
import src.systems.scores as scores
from src.settings import SCREEN_W, SCREEN_H, HUD_FONT_SIZE, HUD_COLOR


class ScoresScene:
    def __init__(self, game):
        self._game = game
        self._font_large = pygame.font.SysFont(None, 60)
        self._font = pygame.font.SysFont(None, HUD_FONT_SIZE)
        self._scores = scores.load()

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                    self._game.pop_scene()

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        cx = SCREEN_W // 2

        title = self._font_large.render("HIGH SCORES", True, (255, 220, 0))
        screen.blit(title, (cx - title.get_width() // 2, 60))

        if not self._scores:
            empty = self._font.render("NO SCORES YET", True, (180, 180, 180))
            screen.blit(empty, (cx - empty.get_width() // 2, SCREEN_H // 2))
        else:
            for i, entry in enumerate(self._scores):
                color = (255, 255, 255) if i == 0 else HUD_COLOR
                line = f"{i + 1:>2}. {entry['initials']:<3}  {entry['score']:>8}"
                surf = self._font.render(line, True, color)
                screen.blit(surf, (cx - surf.get_width() // 2, 160 + i * 40))

        hint = self._font.render("PRESS ESC/SPACE TO BACK", True, (100, 100, 100))
        screen.blit(hint, (cx - hint.get_width() // 2, SCREEN_H - 60))
