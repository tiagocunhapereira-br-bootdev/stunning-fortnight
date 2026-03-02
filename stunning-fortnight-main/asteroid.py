from constants import *
from circleshape import CircleShape
import pygame
import random
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.wrap_position()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_velocity_1 = self.velocity.rotate(random_angle)
        new_velocity_2 = self.velocity.rotate(-random_angle)
        first_asteroid  = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity  = new_velocity_1  * 1.2
        second_asteroid.velocity = new_velocity_2 * 1.2

    def handle_hit(self):
        self.split()
        return 5
