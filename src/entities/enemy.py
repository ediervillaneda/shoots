import pygame
from src.settings import SCREEN_H


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, w, h, color, hp, points):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(centerx=x, bottom=0)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.hp = hp
        self.points = points

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

    def update(self, dt):
        if self.rect.top > SCREEN_H:
            self.kill()

    def death_burst(self, count: int = None) -> list:
        """Retorna `count` EnemyBullet en 360° desde la posición actual."""
        from src.entities.enemy_bullet import EnemyBullet
        from src.settings import DEATH_BURST_COUNT
        if count is None:
            count = DEATH_BURST_COUNT
        cx = self.rect.centerx
        cy = self.rect.centery
        bullets = []
        for i in range(count):
            angle = 360.0 * i / count
            bullets.append(EnemyBullet(cx, cy, angle))
        return bullets
