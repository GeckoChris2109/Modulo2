import random
from dino_runner.utils.constants import SCREEN_WIDTH, CLOUD
class Cloud:
    def __init__(self):
        self.image = CLOUD
        self.width = self.image.get_width()
        self.cloud_x = SCREEN_WIDTH + random.randint(250, 600)
        self.cloud_y = random.randint(50, 300)

    def update(self, game_speed):
        self.cloud_x -= game_speed
        if self.cloud_x < -self.width:
            self.cloud_x = SCREEN_WIDTH + random.randint(200, 600)
            self.cloud_y = random.randint(50, 100)

    
    def draw(self, screen):
        screen.blit(self.image, (self.cloud_x, self.cloud_y))