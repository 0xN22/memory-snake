import pygame
import time
import random


# -------------------------------------------------------------------------------------------- #
# Variables
cell_size = 20
game_speed = 10

pygame.init()

# Windows Size
window_x = 720
window_y = 480

screen = pygame.display.set_mode((window_x, window_y))

# Font
font = pygame.font.SysFont('Comic Sans MS', 30)

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)

# FPS
fps = pygame.time.Clock()

# -------------------------------------------------------------------------------------------- #
# Outer loop - runs once per full game (handles restart)
while True:

    # ---- Reset everything for a fresh game ----
    snake_body = [[100, 80], [80, 80], [60, 80]]
    move_x = cell_size
    move_y = 0
    food_position = [random.randrange(0, window_x, cell_size), random.randrange(80, window_y, cell_size)]
    bomb_positions = []
    score = 0
    bomb_hits = 0
    level = 1
    food_this_level = 0

    game_over = False

    # ---- Inner loop - the actual game, runs every frame ----
    while True:
        snake_body.insert(0, [snake_body[0][0] + move_x, snake_body[0][1] + move_y])

        # Check if the snake has hit the boundaries of the window
        if snake_body[0][0] >= window_x or snake_body[0][1] < 60 or snake_body[0][1] >= window_y or snake_body[0][0] < 0:
            text_surface = font.render("Game Over!", False, (0, 255, 0))
            screen.blit(text_surface, (window_x // 2 - text_surface.get_width() // 2, window_y // 2 - text_surface.get_height() // 2))
            pygame.display.flip()
            time.sleep(2)
            game_over = True
            break

        screen.fill(black)
        # Draw score
        score_surface = font.render("Score: " + str(score), False, (0, 255, 0))
        screen.blit(score_surface, (window_x // 2 - score_surface.get_width() // 2, 10))
        pygame.draw.line(screen, white, (0, 60), (window_x, 60))
        # Draw level
        level_surface = font.render("Level " + str(level), False, (0, 255, 0))
        screen.blit(level_surface, (10, 10))

        # ---------------------------------------------------------------------------------- #
        # Eat mechanic
        if snake_body[0][0] == food_position[0] and snake_body[0][1] == food_position[1]:
            food_position = [random.randrange(0, window_x, cell_size), random.randrange(80, window_y, cell_size)]
            score += 1
            food_this_level += 1
        else:
            snake_body.pop()

        # ---------------------------------------------------------------------------------- #
        # Level mechanics
        if level <= 5:
            food_needed = 5
        else:
            food_needed = 3

        if food_this_level >= food_needed:
            # bomb mechanic
            bomb_count = (level + 1) // 2
            bomb_positions = []
            for i in range(bomb_count):
                bomb_positions.append([random.randrange(0, window_x, cell_size), random.randrange(80, window_y, cell_size)])
            level += 1
            food_this_level = 0

            # Show bombs briefly before blackout
            for bomb in bomb_positions:
                pygame.draw.circle(screen, yellow, (bomb[0], bomb[1]), 10)
            pygame.display.flip()
            time.sleep(1.5)

            # Blackout
            screen.fill(black)
            pygame.display.flip()
            time.sleep(1)

        # ---------------------------------------------------------------------------------- #
        # Dictates how fast the snake goes
        pygame.time.delay(100)
        self_collision = False
        # Check if the head has collided with any part of the snake's own body (excluding the head itself)
        for part in snake_body[1:]:
            if part[0] == snake_body[0][0] and part[1] == snake_body[0][1]:
                text_surface = font.render("Game Over!", False, (0, 255, 0))
                screen.blit(text_surface, (window_x // 2 - text_surface.get_width() // 2, window_y // 2 - text_surface.get_height() // 2))
                pygame.display.flip()
                time.sleep(2)
                self_collision = True
        if self_collision:
            game_over = True
            break

        # Collisions
        bomb_collision = False
        for bomb in bomb_positions:
            if bomb[0] == snake_body[0][0] and bomb[1] == snake_body[0][1]:
                bomb_collision = True

        if bomb_collision:
            bomb_hits += 1

            if bomb_hits == 1 and score > 2:
                penalty = 0.5
            elif bomb_hits == 2 and score > 5:
                penalty = 0.8
            elif bomb_hits == 3:
                penalty = 0.95
            elif bomb_hits > 3:
                game_over = True
                text_surface = font.render("Game Over!", False, (0, 255, 0))
                screen.blit(text_surface, (window_x // 2 - text_surface.get_width() // 2, window_y // 2 - text_surface.get_height() // 2))
                pygame.display.flip()
                time.sleep(2)
                break   
            else:
                penalty = 0

            segments_to_remove = int(len(snake_body) * penalty)

            for segment in range(segments_to_remove):
                snake_body.pop()

            if len(snake_body) == 0:
                text_surface = font.render("Game Over!", False, (0, 255, 0))
                screen.blit(text_surface, (window_x // 2 - text_surface.get_width() // 2, window_y // 2 - text_surface.get_height() // 2))
                pygame.display.flip()
                time.sleep(2)
                game_over = True
                break

        # ---------------------------------------------------------------------------------- #
        # Draw the snake body + movement
        for part in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(part[0], part[1], cell_size, cell_size))
        # Draw food
        pygame.draw.rect(screen, red, pygame.Rect(food_position[0], food_position[1], cell_size, cell_size))

        # Keyboard inputs - for LEFT/RIGHT, UP/DOWN
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if move_x != cell_size:
                    if event.key == pygame.K_LEFT:
                        move_x = -cell_size
                        move_y = 0
                if move_x != -cell_size:
                    if event.key == pygame.K_RIGHT:
                        move_x = cell_size
                        move_y = 0
                if move_y != -cell_size:
                    if event.key == pygame.K_DOWN:
                        move_x = 0
                        move_y = cell_size
                if move_y != cell_size:
                    if event.key == pygame.K_UP:
                        move_x = 0
                        move_y = -cell_size

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()

    # ---- Game over: show restart prompt ----
    if game_over:
        restart_surface = font.render("Press SPACE to restart or ESC to quit", False, white)
        screen.blit(restart_surface, (window_x // 2 - restart_surface.get_width() // 2, window_y // 2 + 40))
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_input = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()