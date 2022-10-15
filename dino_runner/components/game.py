from email import message
import pygame

from dino_runner.components.cloud import Cloud
from dino_runner.utils.constants import COLOURS, RESET, DINO_DEAD, GAME_OVER, BG, ICON , SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.running = False
        self.score = 0
        self.hi_score = 0
        self.death_count = 0
        self.cloud = Cloud()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.reset_game()
        
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.cloud.update(self.game_speed)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.cloud.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def reset_game(self):
        self.score = 0
        self.obstacle_manager.reset_obstacles()

    def draw_score(self):
        self.message1(f'Score {self.score}', 100 , 50)

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 900:
            self.game_speed += 5

        if self.score > self.hi_score:
            self.hi_score = self.score

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def message1(self, txt, x, y):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(txt, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (x , y)
        self.screen.blit(text, text_rect)

    def show_menu(self):
        self.screen.fill(COLOURS['purple'])
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            self.message1("Press any key for start", half_screen_width, half_screen_height)
        else:
            self.screen.blit(DINO_DEAD, (half_screen_width - 20, half_screen_height - 140))
            self.text = "Play again?  " f'Deaths: {self.death_count}'   
            self.message1(self.text, half_screen_width, half_screen_height)
            
            self.screen.blit(RESET, (half_screen_width -20, half_screen_height +50))
            
            self.text = f'Score: {self.score}'
            self.message1(self.text, 100, 50)
            self.screen.blit(GAME_OVER, (half_screen_width -180, half_screen_height -250))

        pygame.display.update()
        self.handle_events_on_menu()
