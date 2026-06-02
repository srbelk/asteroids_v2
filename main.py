import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shots import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # initialize the the game
    pygame.init()

    # game_clock object,tracks time in miliseconds
    game_clock = pygame.time.Clock()

    # delta time tracks the amount of time between  drawn frames
    dt = 0.0

    # screen object, what being used to present the game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # group of sprites that can update
    updatable = pygame.sprite.Group()

    # group of sprites that can be drawn
    drawable = pygame.sprite.Group()

    # assign sprites with the Player class to groups
    Player.containers = (updatable, drawable)

    # player object, sprite representing the user
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # group of sprites considered shots
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)

    # group of sprites that are considered asteroids
    asteroids = pygame.sprite.Group()

    # assign sprites with the Asteroid class to groups
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = updatable

    asteroidfield = AsteroidField()

    # game event loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # make the screen black
        screen.fill("black")

        # update sprites position
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        # add sprites to screen
        for sprite in drawable:
            sprite.draw(screen)

        # present the screen to user
        pygame.display.flip()

        # re-assign dt variable. calculates frames in seconds
        dt = game_clock.tick(60) / 1000


if __name__ == "__main__":
    main()
