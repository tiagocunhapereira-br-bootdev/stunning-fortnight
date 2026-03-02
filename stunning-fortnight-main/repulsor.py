import pygame

class RepulsorWave(pygame.sprite.Sprite):
    def __init__(self, player, asteroids):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
            
        self.player = player
        self.asteroids = asteroids
        
        # Wave settings
        self.current_radius = 0
        self.max_radius = 400.0
        self.expansion_speed = 1200.0 # Pixels per second
        self.force = 600.0 # How fast the asteroids fly away

    def update(self, dt):
        # 1. Expand the wave
        self.current_radius += self.expansion_speed * dt
        
        # 2. Check for asteroids caught in the wave front
        for asteroid in self.asteroids:
            dist = self.player.position.distance_to(asteroid.position)
            
            # If the asteroid is roughly at the edge of our expanding wave
            if abs(dist - self.current_radius) < 20: 
                # Calculate the "Away" vector
                direction = (asteroid.position - self.player.position).normalize()
                # Apply the repulsor force
                asteroid.velocity = direction * self.force

        # 3. Kill the sprite when it reaches max size
        if self.current_radius >= self.max_radius:
            self.kill()

    def draw(self, screen):
        # Draw an expanding cyan ring
        if self.current_radius > 0:
            pygame.draw.circle(
                screen, 
                (0, 255, 255), 
                self.player.position, 
                int(self.current_radius), 
                2 # Width of the ring
            )
