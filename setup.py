import pygame
import sys
import random
import numpy as np

def change_color():
    new_color = list(np.random.randint(0, 256, 3))
    return new_color

def ball_animation():
    global ball_y_speed, ball_x_speed, player_score, opponent_score, ball_color, score_time

    ball.x += ball_x_speed
    ball.y += ball_y_speed

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_y_speed *= -1
        ball_color = change_color()

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_color = change_color()
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        ball_color = change_color()
        score_time = pygame.time.get_ticks()


    if ball.colliderect(player) and ball_x_speed > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_x_speed *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_y_speed < 0:
            ball_y_speed *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_y_speed > 0:
            ball_y_speed *= -1

        ball_color = change_color()

    if ball.colliderect(opponent) and ball_x_speed < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_x_speed *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_y_speed < 0:
            ball_y_speed *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_y_speed > 0:
            ball_y_speed *= -1

        ball_color = change_color()

def ball_restart():
    global ball_x_speed, ball_y_speed, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render('3', False, black)
        screen.blit(number_three, (screen_width/2 - 5, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render('2', False, black)
        screen.blit(number_two, (screen_width/2 - 5, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render('1', False, black)
        screen.blit(number_one, (screen_width/2 - 5, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_x_speed, ball_y_speed = 0, 0
    else:
        ball_x_speed = 7 * random.choice((1, -1))
        ball_y_speed = 7 * random.choice((1, -1))
        score_time = None

def player_animation():
    global player_speed
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    global opponent_speed
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

# general setup
pygame.init()
clock = pygame.time.Clock()

# main window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# objects
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 10, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(0, screen_height/2 - 70, 10, 140)
# scoreboard = pygame.Rect(screen_width/2 - 65, 10, 130, 30)

# colors
bg_color = [191, 191, 191]
black = [0, 0, 0]
red = [150, 21, 28]
purple = [154, 55, 240]
cyan = [35, 186, 216]
ball_color = cyan
# scoreboard_color = bg_color

# speeds
ball_x_speed = 7 * random.choice((1, -1))
ball_y_speed = 7 * random.choice((1, 1))
player_speed = 0
opponent_speed = 7

# text variable
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 25)

# score timer
score_time = True

# sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

while True:
    # handling output
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # game logic
    ball_animation()
    player_animation()
    opponent_animation()

    # visuals
    screen.fill(bg_color)
    # pygame.draw.rect(screen, scoreboard_color, scoreboard)
    pygame.draw.rect(screen, purple, player)
    pygame.draw.rect(screen, red, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, black, (screen_width/2, 0), (screen_width/2, screen_height))

    if score_time:
        ball_restart()

    player_text = game_font.render(f'{player_score}', False, black)
    screen.blit(player_text, (670, 11))
    opponent_text = game_font.render(f'{opponent_score}', False, black)
    screen.blit(opponent_text, (600, 11))


    # updating the window
    pygame.display.flip()
    clock.tick(60)
