import pygame
from src.settings import SCREEN_W, SCREEN_H, HUD_COLOR


_TITLE_COLOR = (255, 220, 0)
_OPTION_COLOR = (180, 180, 180)
_SELECTED_COLOR = (255, 255, 0)

_OPTIONS = ["JUGAR", "RECORDS", "SALIR"]


class MenuScene:
    def __init__(self, game):
        self._game = game
        self._font_title = pygame.font.SysFont(None, 80)
        self._font = pygame.font.SysFont(None, 48)
        self._selected = 0

    def process_input(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_UP, pygame.K_w):
                self._selected = (self._selected - 1) % len(_OPTIONS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._selected = (self._selected + 1) % len(_OPTIONS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._activate()
            elif event.key == pygame.K_ESCAPE:
                self._game.pop_scene()

    def _activate(self):
        if self._selected == 0:   # JUGAR
            from src.scenes.gameplay import GameplayScene
            self._game.push_scene(GameplayScene(self._game))
        elif self._selected == 1:  # RECORDS
            from src.scenes.scores_scene import ScoresScene
            self._game.push_scene(ScoresScene(self._game))
        elif self._selected == 2:  # SALIR
            self._game.pop_scene()

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        cx = SCREEN_W // 2
        cy = SCREEN_H // 2

        title = self._font_title.render("STARFALL", True, _TITLE_COLOR)
        screen.blit(title, (cx - title.get_width() // 2, cy - 220))

        subtitle = pygame.font.SysFont(None, 28).render(
            "SHOOT 'EM UP", True, (150, 150, 150))
        screen.blit(subtitle, (cx - subtitle.get_width() // 2, cy - 140))

        for i, option in enumerate(_OPTIONS):
            color = _SELECTED_COLOR if i == self._selected else _OPTION_COLOR
            surf = self._font.render(option, True, color)
            screen.blit(surf, (cx - surf.get_width() // 2, cy - 40 + i * 70))
