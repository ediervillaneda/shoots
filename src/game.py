import pygame
import src.systems.audio as audio
from src.settings import SCREEN_W, SCREEN_H, FPS, TITLE


class Game:
    def __init__(self):
        pygame.init()
        audio.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self._stack: list = []
        self._running = True
        # Import aquí para evitar circular imports
        from src.scenes.menu import MenuScene
        self.push_scene(MenuScene(self))

    def push_scene(self, scene) -> None:
        self._stack.append(scene)

    def pop_scene(self) -> None:
        self._stack.pop()
        if not self._stack:
            self._running = False

    def replace_scene(self, scene) -> None:
        self._stack[-1] = scene

    def run(self):
        while self._running and self._stack:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
            scene = self._stack[-1]
            scene.process_input(events)
            scene.update(dt)
            scene.render(self.screen)
            pygame.display.flip()
        pygame.quit()
