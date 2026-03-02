import pygame

class RailgunBeam(pygame.sprite.Sprite):
    def __init__(self, player, targets):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
            
        self.player = player
        self.targets = targets

        # Initial stats
        self.current_width = 100.0
        # Fades over 0.2 seconds (40 / 0.2 = 200)
        self.decay_rate = 200.0 

    def update(self, dt):
        # 1. Decay the width
        self.current_width -= dt * self.decay_rate
        if self.current_width <= 0:
            self.kill()
            return

        # 2. Update the beam's geometry to follow the ship
        direction = pygame.Vector2(0, 1).rotate(self.player.rotation)
        start_pos = self.player.position
        end_pos = self.player.position + (direction * 2000)

        # 3. Collision logic for the "Sweep"
        for target in self.targets:
            vec_to_asteroid = target.position - start_pos
            proj_len = vec_to_asteroid.dot(direction)
            
            if proj_len > 0:
                closest_point = start_pos + (direction * proj_len)
                dist = closest_point.distance_to(target.position)
                
                # Use current width for the hitbox
                if dist < target.radius + (self.current_width / 2):
                    # This is the line you are looking for!
                    target.handle_hit()


    def draw(self, screen):
        if self.current_width >= 1:
            # Recalculate positions for drawing so it's frame-perfect
            direction = pygame.Vector2(0, 1).rotate(self.player.rotation)
            start_pos = self.player.position
            end_pos = self.player.position + (direction * 2000)
            
            pygame.draw.line(
                screen, 
                (0, 200, 255), # The color a railgun shot is depicted as
                start_pos, 
                end_pos, 
                int(self.current_width)
            )
