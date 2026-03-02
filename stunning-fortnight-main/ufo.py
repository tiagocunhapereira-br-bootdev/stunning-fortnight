import pygame
import random
from circleshape import CircleShape
from constants import *
import math

class UFOShot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, 2)
            
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.radius = 2 # Small, like the player's shots

    def update(self, dt):
        self.position += self.velocity * dt
        # UFO shots should also wrap!
        self.wrap_position()

    def draw(self, screen):
        # Use a distinct "Hostile" color like bright Red or Orange
        # (surface, color, center, radius, width)
        pygame.draw.circle(screen, (255, 50, 50), self.position, self.radius)

class UFO(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 30)
        self.health = 10
        self.velocity = pygame.Vector2(random.uniform(-150, 150), random.uniform(-50, 50))
        self.shoot_timer = 2.0 # Fires every 2 seconds

    def draw(self, screen):
        points = []
        for i in range(6):
            # Calculate the angle for each vertex (60 degrees apart)
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
        
            # Calculate the x and y coordinates
            x = self.position.x + self.radius * math.cos(angle_rad)
            y = self.position.y + self.radius * math.sin(angle_rad)
            points.append((x, y))
    
        # Draw the hexagon as a polygon
        # (surface, color, points, width)
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

    def update(self, dt, asteroid_group, player_pos):
        self.position += self.velocity * dt
        self.wrap_position()
        
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.shoot(asteroid_group, player_pos)
            self.shoot_timer = 2.0

    def shoot(self, asteroid_group, player_pos):
        # 50% chance to target an asteroid, 50% to target the player
        if random.random() < 0.5 and len(asteroid_group) > 0:
            target = random.choice(asteroid_group.sprites())
            target_pos = target.position
        else:
            target_pos = player_pos

        # Calculate direction and spawn a projectile
        direction = (target_pos - self.position).normalize()
        # Note: Use a separate group or flag so the UFO doesn't shoot itself
        UFOShot(self.position.x, self.position.y, direction * 400)
    def handle_hit(self):
        destroyed = self.take_damage(1)
        if destroyed:
            return 200 # Big points for the kill
        return 10 # Small points for the hit
