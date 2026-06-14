import pygame
import src.systems.audio as audio
from src.settings import SCREEN_W, SCREEN_H, FPS, TITLE
from src.scenes.gameplay import GameplayScene


class Game:
    def __init__(self):
        pygame.init()
        audio.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.scene = GameplayScene()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            self.scene.process_input(events)
            self.scene.update(dt)
            self.scene.render(self.screen)
            pygame.display.flip()
        pygame.quit()
