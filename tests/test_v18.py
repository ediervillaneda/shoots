"""Tests for v1.8.0 — advanced enemy shots: Gunner burst, death_burst, HomingBullet, lead shot."""
import math
import pytest
import pygame
from src.entities.gunner import Gunner
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.entities.homing_bullet import HomingBullet
from src.entities.interceptor import Interceptor
from src.entities.striker import Striker
from src.settings import (
    BURST_COUNT,
    BURST_INTERVAL_MS,
    BURST_PAUSE_MS,
    DEATH_BURST_COUNT,
    HOMING_BULLET_SPEED,
    INTERCEPTOR_SHOOT_INTERVAL,
    STRIKER_SHOOT_INTERVAL,
    PLAYER_SPEED,
    LEAD_TIME_S,
)


# ---- Gunner burst ----

class TestGunnerBurst:
    def test_initial_burst_state(self):
        g = Gunner(270)
        assert g._burst_idx == 0
        assert g._next_burst_ms == 0

    def test_shoot_returns_3_bullets(self):
        g = Gunner(270)
        bullets = g.shoot(1000)
        assert len(bullets) == 3

    def test_shoot_bullets_are_enemy_bullets(self):
        g = Gunner(270)
        bullets = g.shoot(1000)
        assert all(isinstance(b, EnemyBullet) for b in bullets)

    def test_burst_idx_increments_after_shot(self):
        g = Gunner(270)
        g.shoot(1000)
        assert g._burst_idx == 1

    def test_next_burst_ms_set_to_interval_after_first_shot(self):
        g = Gunner(270)
        g.shoot(1000)
        assert g._next_burst_ms == 1000 + BURST_INTERVAL_MS

    def test_no_shoot_before_interval(self):
        g = Gunner(270)
        g.shoot(1000)
        # 40ms later — less than BURST_INTERVAL_MS=80
        result = g.shoot(1040)
        assert result == []

    def test_burst_pause_after_full_burst(self):
        """After BURST_COUNT shots, _burst_idx resets and pause is applied."""
        g = Gunner(270)
        now = 0
        for _ in range(BURST_COUNT):
            g.shoot(now)
            now += BURST_INTERVAL_MS
        assert g._burst_idx == 0
        assert g._next_burst_ms == (now - BURST_INTERVAL_MS) + BURST_PAUSE_MS

    def test_no_shoot_during_pause(self):
        g = Gunner(270)
        now = 0
        for _ in range(BURST_COUNT):
            g.shoot(now)
            now += BURST_INTERVAL_MS
        # immediately after the last shot — still in pause window
        result = g.shoot(now)
        assert result == []

    def test_resumes_after_pause(self):
        g = Gunner(270)
        now = 0
        for _ in range(BURST_COUNT):
            g.shoot(now)
            now += BURST_INTERVAL_MS
        # advance past the pause
        now += BURST_PAUSE_MS
        bullets = g.shoot(now)
        assert len(bullets) == 3


# ---- Enemy.death_burst ----

class TestDeathBurst:
    def test_default_count_is_death_burst_count(self):
        from src.entities.scout import Scout
        s = Scout(270)
        bullets = s.death_burst()
        assert len(bullets) == DEATH_BURST_COUNT

    def test_all_bullets_are_enemy_bullet_instances(self):
        from src.entities.scout import Scout
        s = Scout(270)
        bullets = s.death_burst()
        assert all(isinstance(b, EnemyBullet) for b in bullets)

    def test_custom_count(self):
        from src.entities.scout import Scout
        s = Scout(270)
        bullets = s.death_burst(count=4)
        assert len(bullets) == 4

    def test_angles_are_evenly_spread(self):
        """For count=4, angles should be 0, 90, 180, 270 degrees."""
        from src.entities.scout import Scout
        s = Scout(270)
        bullets = s.death_burst(count=4)
        # Each bullet's velocity encodes the angle via sin/cos
        expected_angles = [0.0, 90.0, 180.0, 270.0]
        for b, expected_deg in zip(bullets, expected_angles):
            rad = math.radians(expected_deg)
            # vx = sin(angle)*speed, vy = cos(angle)*speed
            from src.settings import ENEMY_BULLET_SPEED
            assert abs(b._vx - math.sin(rad) * ENEMY_BULLET_SPEED) < 0.5
            assert abs(b._vy - math.cos(rad) * ENEMY_BULLET_SPEED) < 0.5

    def test_bullets_originate_from_enemy_center(self):
        from src.entities.scout import Scout
        s = Scout(270)
        cx = s.rect.centerx
        cy = s.rect.centery
        bullets = s.death_burst()
        for b in bullets:
            # rect is placed with centerx and top=y, so centerx should match
            assert b.rect.centerx == cx


# ---- HomingBullet ----

class TestHomingBullet:
    def test_is_enemy_bullet_subclass(self):
        hb = HomingBullet(270, 100, 0, None)
        assert isinstance(hb, EnemyBullet)

    def test_speed_uses_homing_bullet_speed(self):
        """Velocity magnitude should equal HOMING_BULLET_SPEED, not ENEMY_BULLET_SPEED."""
        hb = HomingBullet(270, 100, 0, None)
        speed = math.hypot(hb._vx, hb._vy)
        assert abs(speed - HOMING_BULLET_SPEED) < 0.5

    def test_no_target_velocity_unchanged(self):
        """Without a target, velocity components remain constant after update."""
        hb = HomingBullet(270, 100, 0, None)
        vx_before = hb._vx
        vy_before = hb._vy
        hb.update(0.016)
        assert abs(hb._vx - vx_before) < 0.01
        assert abs(hb._vy - vy_before) < 0.01

    def test_with_dead_target_velocity_unchanged(self):
        """A killed target is treated as no target — velocity stays constant."""
        from src.entities.scout import Scout
        target = Scout(270)
        hb = HomingBullet(270, 100, 90, target)
        target.kill()
        vx_before = hb._vx
        vy_before = hb._vy
        hb.update(0.016)
        assert abs(hb._vx - vx_before) < 0.01
        assert abs(hb._vy - vy_before) < 0.01


# ---- Interceptor uses HomingBullet ----

class TestInterceptorHomingBullet:
    def test_shoot_returns_homing_bullet(self):
        inter = Interceptor(270)
        inter._entry_done = True
        bullets = inter.shoot(INTERCEPTOR_SHOOT_INTERVAL)
        assert len(bullets) == 1
        assert isinstance(bullets[0], HomingBullet)

    def test_no_shoot_during_entry_phase(self):
        inter = Interceptor(270)
        # _entry_done defaults to False
        assert inter.shoot(0) == []


# ---- Striker lead shot ----

class TestStrikerLeadShot:
    def _make_mock_target(self, centerx, centery, vel_x, vel_y=0.0):
        """Minimal mock with rect and velocity attributes."""
        class MockTarget:
            def __init__(self):
                self.rect = pygame.Rect(0, 0, 32, 32)
                self.rect.centerx = centerx
                self.rect.centery = centery
                self.vel_x = vel_x
                self.vel_y = vel_y
        return MockTarget()

    def test_lead_shot_differs_from_direct_aim_when_target_moving(self):
        """Angle to predicted position != angle to current position when target moves."""
        s = Striker(270)
        s.y = 300.0
        s.rect.y = 300

        cx = s.rect.centerx
        bottom = s.rect.bottom

        target = self._make_mock_target(centerx=270, centery=500, vel_x=1.0)
        s.target = target
        s.last_shot = -STRIKER_SHOOT_INTERVAL

        # Direct angle (no lead)
        direct_dx = target.rect.centerx - cx
        direct_dy = target.rect.centery - bottom
        direct_angle = math.degrees(math.atan2(direct_dx, max(1, direct_dy)))

        # Predicted angle
        pred_x = target.rect.centerx + target.vel_x * PLAYER_SPEED * LEAD_TIME_S
        lead_dx = pred_x - cx
        lead_angle = math.degrees(math.atan2(lead_dx, max(1, direct_dy)))

        bullets = s.shoot(STRIKER_SHOOT_INTERVAL)
        # Striker fires two bullets offset ±10° from lead_angle
        assert len(bullets) == 2
        # The lead angle should differ from the direct angle
        assert abs(lead_angle - direct_angle) > 0.1

    def test_no_lead_when_target_stationary(self):
        """When vel_x=0, lead angle equals direct angle."""
        s = Striker(270)
        s.y = 300.0
        s.rect.y = 300
        s.last_shot = -STRIKER_SHOOT_INTERVAL

        target = self._make_mock_target(centerx=200, centery=500, vel_x=0.0)
        s.target = target

        cx = s.rect.centerx
        bottom = s.rect.bottom
        direct_dx = target.rect.centerx - cx
        direct_dy = target.rect.centery - bottom
        direct_angle = math.degrees(math.atan2(direct_dx, max(1, direct_dy)))

        bullets = s.shoot(STRIKER_SHOOT_INTERVAL)
        assert len(bullets) == 2
        # Both bullets are at direct_angle ± 10
        angles = [direct_angle - 10, direct_angle + 10]
        for b, expected_angle in zip(bullets, angles):
            rad = math.radians(expected_angle)
            from src.settings import ENEMY_BULLET_SPEED
            assert abs(b._vx - math.sin(rad) * ENEMY_BULLET_SPEED) < 1.0
