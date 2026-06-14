import pygame
import src.systems.scores as scores
from src.settings import SCREEN_W, SCREEN_H, HUD_FONT_SIZE, HUD_COLOR


class GameOverScene:
    def __init__(self, game, score: int):
        self._game = game
        self._score = score
        self._font_large = pygame.font.SysFont(None, 72)
        self._font = pygame.font.SysFont(None, HUD_FONT_SIZE)
        self._scores = scores.load()
        self._is_highscore = scores.qualifies(score, self._scores)
        self._initials = ""
        self._saved = False

    def process_input(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            key = event.key

            if self._is_highscore and not self._saved:
                if key == pygame.K_BACKSPACE:
                    self._initials = self._initials[:-1]
                elif key == pygame.K_RETURN:
                    if self._initials:
                        self._scores = scores.save(
                            self._initials, self._score, self._scores
                        )
                        self._saved = True
                elif len(self._initials) < 3 and event.unicode.isalpha():
                    self._initials += event.unicode.upper()
            else:
                if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                    from src.scenes.menu import MenuScene
                    self._game.replace_scene(MenuScene(self._game))

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        cx = SCREEN_W // 2
        cy = SCREEN_H // 2

        title = self._font_large.render("GAME OVER", True, (220, 50, 50))
        screen.blit(title, (cx - title.get_width() // 2, cy - 180))

        score_surf = self._font.render(
            f"SCORE: {self._score}", True, HUD_COLOR)
        screen.blit(score_surf, (cx - score_surf.get_width() // 2, cy - 100))

        if self._is_highscore and not self._saved:
            prompt = self._font.render("TOP 10! ENTER INITIALS:", True, (255, 255, 0))
            screen.blit(prompt, (cx - prompt.get_width() // 2, cy - 40))
            initials_surf = self._font_large.render(
                self._initials + "_", True, (255, 255, 255))
            screen.blit(initials_surf, (cx - initials_surf.get_width() // 2, cy + 10))
        elif self._saved:
            saved_surf = self._font.render("SAVED! PRESS ENTER/SPACE", True, (100, 255, 100))
            screen.blit(saved_surf, (cx - saved_surf.get_width() // 2, cy - 20))
        else:
            hint = self._font.render("PRESS ENTER/SPACE TO CONTINUE", True, (180, 180, 180))
            screen.blit(hint, (cx - hint.get_width() // 2, cy - 20))
