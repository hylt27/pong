import pygame
import sys
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

class Ball(Block):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed, paddles):
        super().__init__(path, x_pos, y_pos)
        self.x_speed = x_speed * random.choice((-1, 1))
        self.y_speed = y_speed * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.y_speed *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.x_speed > 0:
                self.x_speed *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.x_speed < 0:
                self.x_speed *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.y_speed > 0:
                self.rect.bottom = collision_paddle.top
                self.y_speed *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.y_speed < 0:
                self.rect.top = collision_paddle.bottom
                self.y_speed *= -1

    def reset_ball(self):
        self.active = False
        self.x_speed *= random.choice((-1, 1))
        self.y_speed *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2, screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1

        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = game_font.render(str(countdown_number), True, black)
        time_counter_rect = time_counter.get_rect(center=(screen_width/2, screen_height/2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

class GameManager:

    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # drawing game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # updating game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(str(self.player_score), True, black)
        opponent_score = game_font.render(str(self.opponent_score), True, black)

        player_score_rect = player_score.get_rect(midleft=(screen_width/2 + 40, screen_height/2))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width/2 - 40, screen_height/2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

# general setup
pygame.init()
clock = pygame.time.Clock()

# main window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')


# global variables
bg_color = [191, 191, 191]
black = [0, 0, 0]
cyan = [35, 186, 216]
game_font = pygame.font.Font("freesansbold.ttf", 25)
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)

# objects
player = Player('Paddle.png', x_pos=screen_width - 10, y_pos=screen_height/2, speed=5)
opponent = Opponent('Paddle.png', 10, screen_height/2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png', screen_width/2, screen_height/2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

while True:
    # handling output
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
            if event.key == pygame.K_UP:
                player.movement -= player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed
            if event.key == pygame.K_UP:
                player.movement += player.speed

    # background stuff
    screen.fill(bg_color)
    pygame.draw.rect(screen, black, middle_strip)

    # run the game
    game_manager.run_game()

    # updating the window
    pygame.display.flip()
    clock.tick(120)
