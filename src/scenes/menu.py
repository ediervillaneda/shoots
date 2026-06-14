import pygame


class MenuScene:
    def __init__(self, game):
        self._game = game

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._game.pop_scene()

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
