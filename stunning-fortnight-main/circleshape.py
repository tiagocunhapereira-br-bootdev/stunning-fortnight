import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def collides_with(self, other):
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        if distance < (self.radius + other.radius):
            return True
        else:
            return False 
    def wrap_position(self):
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius

        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
