import pygame
from src.settings import SCREEN_H, ENEMY_FLASH_MS, ENEMY_FLASH_ALPHA


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
        self._flash_ms = 0.0
        self._base_image: pygame.Surface | None = None

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
        else:
            self._base_image = self.image.copy()  # capturar sprite real (post-subclass init)
            self._flash_ms = float(ENEMY_FLASH_MS)

    def update(self, dt):
        if self._flash_ms > 0 and self._base_image is not None:
            self._flash_ms -= dt * 1000
            flash = self._base_image.copy()
            flash.fill((255, 255, 255, ENEMY_FLASH_ALPHA), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = flash
        elif self._base_image is not None and self._flash_ms <= 0:
            self.image = self._base_image
            self._base_image = None
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
