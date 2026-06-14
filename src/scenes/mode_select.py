import pygame
from src.settings import SCREEN_W, SCREEN_H, MODE_ENDLESS, MODE_SURVIVAL, MODE_DAILY

_TITLE_COLOR = (255, 220, 0)
_OPTION_COLOR = (180, 180, 180)
_SELECTED_COLOR = (255, 255, 0)

_OPTIONS = [
    (MODE_ENDLESS,  "ENDLESS",  "Dificultad creciente sin fin"),
    (MODE_SURVIVAL, "SURVIVAL", "Sobrevive 3 minutos"),
    (MODE_DAILY,    "DAILY",    "Seed del dia — mismo nivel para todos"),
]


class ModeSelectScene:
    def __init__(self, game):
        self._game = game
        self._font_title = pygame.font.SysFont(None, 60)
        self._font = pygame.font.SysFont(None, 48)
        self._font_sub = pygame.font.SysFont(None, 28)
        self._selected = 0
        self._option_rects: list[pygame.Rect] = []

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self._selected = (self._selected - 1) % len(_OPTIONS)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self._selected = (self._selected + 1) % len(_OPTIONS)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._activate()
                elif event.key == pygame.K_ESCAPE:
                    self._game.pop_scene()
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self._option_rects):
                    if rect.collidepoint(event.pos):
                        self._selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(self._option_rects):
                    if rect.collidepoint(event.pos):
                        self._selected = i
                        self._activate()

    def _activate(self):
        mode = _OPTIONS[self._selected][0]
        from src.scenes.gameplay import GameplayScene
        self._game.push_scene(GameplayScene(self._game, mode=mode))

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        cx = SCREEN_W // 2

        title = self._font_title.render("SELECCIONA MODO", True, _TITLE_COLOR)
        screen.blit(title, (cx - title.get_width() // 2, 120))

        self._option_rects = []
        for i, (_, label, desc) in enumerate(_OPTIONS):
            color = _SELECTED_COLOR if i == self._selected else _OPTION_COLOR
            surf = self._font.render(label, True, color)
            y = 280 + i * 120
            x = cx - surf.get_width() // 2
            screen.blit(surf, (x, y))
            sub = self._font_sub.render(desc, True, (120, 120, 120))
            screen.blit(sub, (cx - sub.get_width() // 2, y + 48))
            self._option_rects.append(pygame.Rect(x - 20, y - 5, surf.get_width() + 40, surf.get_height() + 10))
