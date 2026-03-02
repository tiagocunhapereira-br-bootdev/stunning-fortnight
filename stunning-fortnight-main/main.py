import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from railgun import RailgunBeam
from repulsor import RepulsorWave
from ufo import UFO, UFOShot

def main():
    pygame.init()

    dt = 0

    score = 0

    clocker = pygame.time.Clock()

    updatable = pygame.sprite.Group()

    drawable = pygame.sprite.Group()

    asteroids = pygame.sprite.Group()

    shots = pygame.sprite.Group()

    ufo_shots = pygame.sprite.Group()

    targets = pygame.sprite.Group()

    ufos = pygame.sprite.Group()

    repulsorwaves = pygame.sprite.Group()

    updatable_and_requires_asteroids = pygame.sprite.Group()

    Player.containers = (updatable_and_requires_asteroids, drawable)

    Asteroid.containers = (updatable, drawable, asteroids, targets)

    UFOShot.containers = (drawable, ufo_shots, updatable)

    UFO.containers = (drawable, ufos, targets)

    Shot.containers = (drawable, shots, updatable)

    AsteroidField.containers = (updatable)

    RepulsorWave.containers = (updatable, drawable)

    RailgunBeam.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroidfield = AsteroidField()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    last_ufo_spawn_time = 0  # Track last UFO spawn time
    ufo_spawn_interval = 5000  # 5 seconds in milliseconds

    while True:
        log_state()

        dt = clocker.tick(60) / 1000

        # Spawn UFO every 5 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_ufo_spawn_time > ufo_spawn_interval:
            new_ufo = UFO((SCREEN_WIDTH // 2), 50)  # Example radius value
            last_ufo_spawn_time = current_time

        updatable.update(dt)
        updatable_and_requires_asteroids.update(dt, asteroids, targets)
        ufos.update(dt, asteroids, player.position)

        for target in targets:  # Your supergroup!
            for shot in shots:
                if shot.collides_with(target):
                    # One method to rule them all!
                    score += target.handle_hit()
                    shot.kill()

        for ufo_shot in ufo_shots:
            if player.collides_with(ufo_shot):
                print("Killed by a UFO!")
                sys.exit()  # Or reduce player health!

        for ufo_shot in ufo_shots:
            for asteroid in asteroids:
                if asteroid.collides_with(ufo_shot):
                    asteroid.split()
                    ufo_shot.kill()

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                print(f"Score: {score}")
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
