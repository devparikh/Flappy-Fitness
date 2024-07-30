# import pygame
# from random import randint

# pygame.init()

# SCREEN = pygame.display.set_mode((500, 750))

# Background_image = pygame.image.load('background.jpg')

# bird_image = pygame.image.load('bird1.png')
# bird_x = 50
# bird_y = 300
# bird_y_change = 0
# bird_y_change_factor = 0.5

# def display_bird(bird_image, bird_x, bird_y):
#     SCREEN.blit(bird_image, (bird_x, bird_y))

# obstacle_width = 70
# obstacle_height = randint(150, 450)
# obstacle_color = (211, 253, 117)
# obstacle_x_change_factor = 0.25
# obstacle_x_change = -1
# obstacle_x = 500

# def display_obstacle(object_height, y_pos):
#     pygame.draw.rect(SCREEN, obstacle_color, (obstacle_x, y_pos, obstacle_width, object_height))

# def collision_detection(obstacle_x, obstacle_height, bird_y, bottom_obstacle_height):
#     if obstacle_x >= 50 and obstacle_x <= (50 + 64):
#         if bird_y <= obstacle_height or bird_y >= (bottom_obstacle_height - 64):
#             return True
#         return False
    
# score = 0
# score_font = pygame.font.Font('freesansbold.ttf', 32)

# def score_display(score):
#     display = score_font.render(f"score {score}", True, (255,255,255))
#     SCREEN.blit(display, (10, 10))

# running = True

# while running:
#     SCREEN.fill((0, 0, 0))

#     SCREEN.blit(Background_image, (0, 0))
#     jumped = False
#     for event in pygame.event.get():
#         if jumped:
#             print(jumped)
#             if bird_y_change < 0.5*bird_y_change_factor:
#                 bird_y_change += (0.1*bird_y_change_factor)
#             else:
#                 jumped = False
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 bird_y_change = -1*bird_y_change_factor
#                 jumped = True

#         elif not jumped:
#             bird_y_change = 0.5*bird_y_change_factor

#     bird_y += bird_y_change
#     display_bird(bird_image, bird_x, bird_y)

#     if bird_y <= 0:
#         bird_y = 0
#     if bird_y >= 571:
#         bird_y = 571

#     obstacle_x += obstacle_x_change*obstacle_x_change_factor
#     if obstacle_x <= -10:
#         obstacle_x = 500
#         obstacle_height = randint(200, 400)
#         score += 1
#     display_obstacle(obstacle_height, 0)
#     bottom_obstacle_height = 635 - obstacle_height - 150
#     display_obstacle(bottom_obstacle_height, obstacle_height + 150)

#     collision = collision_detection(obstacle_x, obstacle_height, bird_y, obstacle_height + 150)

#     if collision:
#         pygame.quit()

#     score_display(score)

#     pygame.display.update()

# pygame.quit()

import pygame
from random import randint
import os
import socketio
import threading

pygame.init()
pygame.font.init()

SCREEN = pygame.display.set_mode((500, 750))

Background_image = pygame.image.load('background.jpg')

bird_image = pygame.image.load('bird1.png')

sio = socketio.Client()
did_user_jumped = False

def connect_to_server():
    sio.connect('http://localhost:8000')
    sio.wait()

@sio.event
def connect():
    print('Game connected to server')
    # run_game()

@sio.event
def disconnect():
    print('Disconnected from server')
    pygame.quit()


@sio.event
def flappy_bird_move(data):
    global did_user_jumped
    print("USER JUMPED")
    did_user_jumped = True
    

# connect_to_server()

threading.Thread(target=connect_to_server).start()

bird_x = 50
bird_y = 300
bird_y_change = 0
bird_y_change_factor = 1

def display_bird(bird_image, bird_x, bird_y):
    SCREEN.blit(bird_image, (bird_x, bird_y))

obstacle_width = 70
obstacle_height = randint(150, 450)
obstacle_color = (211, 253, 117)
obstacle_x_change_factor = 0.54
obstacle_x_change = -1
obstacle_x = 500

def display_obstacle(object_height, y_pos):
    pygame.draw.rect(SCREEN, obstacle_color, (obstacle_x, y_pos, obstacle_width, object_height))

def collision_detection(obstacle_x, obstacle_height, bird_y, bottom_obstacle_height):
    if obstacle_x >= 50 and obstacle_x <= (50 + 64):
        if bird_y <= obstacle_height or bird_y >= (bottom_obstacle_height - 64):
            return True
        return False


score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)

def score_display(score):
    display = score_font.render(f"score {score}", True, (255,255,255))
    SCREEN.blit(display, (10, 10))

running = True

started = False
while running:

    SCREEN.fill((0, 0, 0))

    SCREEN.blit(Background_image, (240, 500))
    if not started:
        start = score_font.render('', True, (255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    started = True

        SCREEN.blit(start, (0, 0))

    jumped = False
    for event in pygame.event.get():
        print(did_user_jumped)
        if event.type == pygame.QUIT:
            running = False
    if did_user_jumped:
        print("JUMP found")
        bird_y_change = -60
        print(bird_y)
        did_user_jumped = False
        print(True)
    else:
        bird_y_change = 0.15

    if started:
        bird_y += bird_y_change

        if bird_y <= 0:
            bird_y = 0
        if bird_y > 571:
            bird_y = 571

        obstacle_x += obstacle_x_change*obstacle_x_change_factor
        if obstacle_x <= -10:
            obstacle_x = 500
            obstacle_height = randint(200, 400)
            score += 1
        

        collision = collision_detection(obstacle_x, obstacle_height, bird_y, obstacle_height + 150)

        if collision:
            pygame.quit()

    bottom_obstacle_height = 635 - obstacle_height - 150
    display_obstacle(obstacle_height, 0)
    display_obstacle(bottom_obstacle_height, obstacle_height + 150)
    display_bird(bird_image, bird_x, bird_y)


    score_display(score)

    pygame.display.update()

pygame.quit()

