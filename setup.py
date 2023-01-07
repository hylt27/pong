import pygame
import sys
import random
import numpy as np

def change_color():
    new_color = list(np.random.randint(0, 256, 3))
    return new_color


def ball_animation():
    global ball_x_speed, ball_y_speed, color

    ball.x += ball_x_speed
    ball.y += ball_y_speed

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_y_speed *= -1
        color = change_color()

    if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()
        color = change_color()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_x_speed *= -1
        color = change_color()

def ball_restart():
    global ball_x_speed, ball_y_speed
    ball.center = (screen_width/2, screen_height/2)
    ball_x_speed *= random.choice((1, -1))
    ball_y_speed *= random.choice((1, -1))

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

#objects
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 10, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(0, screen_height/2 - 70, 10, 140)

#colors
bg_color = [191, 191, 191]
black = [0, 0, 0]
red = [150, 21, 28]
purple = [154, 55, 240]
cyan = [35, 186, 216]
color = cyan

#ball speed
ball_x_speed = 7 * random.choice((1, -1))
ball_y_speed = 7 * random.choice((1, 1))
player_speed = 0
opponent_speed = 7

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


    ball_animation()
    player_animation()
    opponent_animation()


    #visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, purple, player)
    pygame.draw.rect(screen, red, opponent)
    pygame.draw.ellipse(screen, color, ball)
    pygame.draw.aaline(screen, black, (screen_width/2,0), (screen_width/2, screen_height))
    
    #updating the window
    pygame.display.flip()
    clock.tick(60)