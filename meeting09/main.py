import pygame
import time
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
cyan = pygame.Color(0, 215, 215)

# Initialise game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
fps = pygame.time.Clock()
snake_speed = 15

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]

# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# setting default snake direction towards right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0
high_score = 0
game_over = False

# Load sounds
try:
    eat_sound = pygame.mixer.Sound('sound.mp3')
    eat_sound.set_volume(0.5)
except:
    print("Warning: sound.mp3 not found. Game will run without sound.")
    eat_sound = None


def show_score(choice, color, font, size):
    """Display score on screen"""
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    game_window.blit(score_surface, score_rect)


def show_game_over():
    """Display game over screen"""
    global game_over, high_score

    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    game_window.blit(game_over_surface, game_over_rect)

    # Show high score
    high_score_font = pygame.font.SysFont('times new roman', 30)
    high_score_surface = high_score_font.render('High Score: ' + str(high_score), True, white)
    high_score_rect = high_score_surface.get_rect()
    high_score_rect.midtop = (window_x / 2, window_y / 2)
    game_window.blit(high_score_surface, high_score_rect)

    pygame.display.flip()
    time.sleep(3)


def reset_game():
    """Reset game variables"""
    global snake_position, snake_body, fruit_position, direction, change_to, score, game_over, fruit_spawn

    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    game_over = False
    fruit_spawn = True


# Main game loop
running = True
while running:

    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_SPACE and game_over:
                reset_game()

    if game_over:
        continue

    # Prevent snake from moving into itself
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))

    # Check if fruit eaten
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
        if eat_sound:
            eat_sound.play()
    else:
        snake_body.pop()

    # Generate new fruit
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

    # Fill background
    game_window.fill(cyan)

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw fruit (circle)
    pygame.draw.circle(game_window, red,
                       (fruit_position[0] + 5, fruit_position[1] + 5), 5)

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over = True
        if score > high_score:
            high_score = score
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over = True
        if score > high_score:
            high_score = score

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over = True
            if score > high_score:
                high_score = score

    # Display score continuously
    show_score(1, white, 'times new roman', 20)

    if game_over:
        show_game_over()

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    fps.tick(snake_speed)

pygame.quit()
quit()