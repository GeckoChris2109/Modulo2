import pygame
import random

from dino_runner.utils.constants import SMALL_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0 , 2) == 0:
                cactus_type = 'SMALL'
                cactus = Cactus(cactus_type)
                self.obstacles.append(cactus) 
            elif random.randint(0 , 2) == 1:
                cactus_type = 'LARGE'
                cactus = Cactus(cactus_type)
                self.obstacles.append(cactus)
                
            elif random.randint(0 , 2) == 2:
                bird = Bird(BIRD)
                self.obstacles.append(bird)

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            if game.player.dino_rect.colliderect(obstacle):
                print('hubo collision')
                pygame.time.delay(1000)
                game.playing = False
                game.score = 0
                game.death_count += 1
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []