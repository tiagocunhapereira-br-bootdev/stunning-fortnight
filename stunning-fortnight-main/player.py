from constants import *
from circleshape import CircleShape
import pygame
from shot import Shot
import random
from railgun import RailgunBeam
from repulsor import RepulsorWave

class Player(CircleShape):
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.x = x
        self.y = y
        self.score = 0
        self.shot_cooldown = 0
        self.shot_spread_cooldown = 0
        self.lightning_timer = 0
        self.railgun_timer = 0
        self.repulsor_timer = 0
        self.hit_asteroids = []

        # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        if self.lightning_timer > 0:
            # 2. Loop through the segments we saved during the fire method
            for start_pos, target_asteroid in self.lightning_segments:
                # 3. Draw the line from the START of the branch to the ASTEROID
                pygame.draw.line(
                    screen, 
                    (0, 255, 255), # Cyan
                    start_pos, 
                    target_asteroid.position, 
                    3 # Width
                )
            
    def update(self, dt, asteroid_group, targets):
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt
        self.shot_spread_cooldown -= dt
        self.lightning_timer -= dt
        self.railgun_timer -= dt
        self.repulsor_timer -= dt
        self.wrap_position()
        if keys[pygame.K_a]:
            self.rotation -= (PLAYER_TURN_SPEED * dt)
        if keys[pygame.K_d]:
            self.rotation += (PLAYER_TURN_SPEED * dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown <= 0:
                self.shoot()
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        if keys[pygame.K_q]:
            if self.shot_spread_cooldown <= 0:
                self.shoot_random_spread()
                self.shot_spread_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS * 6
        if keys[pygame.K_e]:
            if self.lightning_timer <= 0:
                self.fire_storm_lightning(targets)
                self.lightning_timer = PLAYER_SHOOT_COOLDOWN_SECONDS * 6
        if keys[pygame.K_f]:
            if self.railgun_timer <= 0:
                self.fire_railgun(targets)
                self.railgun_timer = PLAYER_SHOOT_COOLDOWN_SECONDS * 25
        if keys[pygame.K_r]: 
            self.fire_repulsor(targets)
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        direction = pygame.Vector2(0, 1)
        direction = direction.rotate(self.rotation)
        direction = direction * SHOT_SPEED
        shot.velocity = direction
    def shoot_random_spread(self):
        for _ in range(10):
            random_angle = self.rotation + random.uniform(-30, 30)
            new_shot = Shot(self.position.x, self.position.y)
            velocity = pygame.Vector2(0, 1).rotate(random_angle)
            new_shot.velocity = velocity * SHOT_SPEED
    def get_nearest_target(self, origin, targets, excluded):
        closest = None
        min_dist = LIGHTNING_RANGE
        for target in targets:
            dist = origin.distance_to(target.position)
            if target in excluded:
                continue
            if dist < min_dist:
                min_dist = dist
                closest = target
        return closest
    def fire_chain_lightning(self, asteroid_group):
        current_origin = self.position
        self.hit_asteroids = []
    
        chaining = True
        while chaining:
            target = self.get_nearest_asteroid(current_origin, asteroid_group, self.hit_asteroids)
    
            if target:
                self.hit_asteroids.append(target)
                current_origin = target.position
        
                # Roll for a 95% chance to KEEP GOING
                # random.random() < 0.95 means "95% of the time, stay in the loop"
                if random.random() > 0.95:
                    chaining = False # Only stop 5% of the time
            else:
                # No more asteroids in range, must stop
                chaining = False
        for asteroid in self.hit_asteroids:
            asteroid.split()
    
        return self.hit_asteroids
    def fire_railgun(self, asteroid_group):
        # 1. Define the beam's direction vector
        # This is a unit vector (length of 1) pointing where the ship is facing
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        start_pos = self.position
        hit_count = 0
        end_pos = self.position + (direction * 2000)
    
        for asteroid in asteroid_group:
            # 2. Vector from ship to asteroid
            vec_to_asteroid = asteroid.position - self.position
        
            # 3. Projection: How far along the beam is the asteroid?
            # Using the Dot Product
            projection_length = vec_to_asteroid.dot(direction)
        
            # We only care about asteroids in FRONT of the ship
            if projection_length > 0:
                # 4. Find the closest point on the beam to the asteroid
                closest_point = self.position + (direction * projection_length)
            
                # 5. Calculate distance from that point to the asteroid's center
                dist = closest_point.distance_to(asteroid.position)
            
                # 6. If distance < radius, it's a hit!
                if dist < asteroid.radius:
                    asteroid.split()
                    hit_count += 1
    
        RailgunBeam(self, asteroid_group)
        return hit_count

    def fire_storm_lightning(self, targets):
        # We use a list to track all active tips of the lightning branches
        sources = [self.position]
        self.lightning_segments = []
        hit_count = 0
        max_hits = 100 # A safety cap is vital for 50% branching!

        while sources and hit_count < max_hits:
            # Take the oldest source point to jump from
            origin = sources.pop(0)
        
            # Get the list of asteroids already claimed by this storm
            hit_list = [seg[1] for seg in self.lightning_segments]
            target = self.get_nearest_target(origin, targets, hit_list)

            if target:
                # Instead of target.split()
                target.handle_hit() 
                self.lightning_segments.append((origin, target))

                # 2. Roll for the "Main" continuation (95% chance)i
                if random.random() < 0.95:
                    sources.append(target.position)
            
                # 3. Roll for the "Branch" split (50% chance)
                # This is an independent check, meaning one hit could 
                # produce 0, 1, or 2 new source points!
                if random.random() < 0.75:
                    sources.append(target.position) 
        self.lightning_timer = 0.1

        return hit_count
    def fire_repulsor(self, asteroids):
        if self.repulsor_timer > 0:
            return
    
        # Spawn the visual wave and logic object
        RepulsorWave(self, asteroids)
    
        # Set a hefty cooldown (e.g., 10 seconds)
        self.repulsor_timer = 10.0
