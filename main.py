# Import necessary libraries
import pygame
import random
import math
from pygame import mixer

# Initialize the pygame library
pygame.init()

# Create the screen (Surface object)
screen = pygame.display.set_mode((800, 600))  # Set screen width to 800 and height to 600

# Background
background = pygame.image.load('icons/BGIMG.jpg')

# Background sound
mixer.music.load('Sounds/Mario_BGM.mp3')
mixer.music.play(-1)

# Set the title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icons/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('icons/space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0  # Variable for vertical movement

# Enemy Alien
enemyImg = pygame.image.load('icons\jadoo.png')  # Only load the image once
enemy_positions = []  # List to hold enemy positions (X, Y)
enemy_x_change = []   # List to hold X-axis movement direction and speed
enemy_y_change = 40   # The distance to move down when an edge is hit
num_of_enemies = random.randint(1, 6)  # Randomly initialize the number of enemies

# Initialize enemy positions and their X-axis movements
for i in range(num_of_enemies):
    enemyX = random.randint(0, 736)
    enemyY = random.randint(50, 150)
    enemy_positions.append([enemyX, enemyY])
    enemy_x_change.append(0.5)  # Start with a small speed

# Bullet
bulletImg = pygame.image.load('icons/bullet_rotate.png')
bulletX = 0  
bulletY = playerY  # Initialize bulletY to start from the player's Y position
bulletY_change = 0.5
bullet_state = "ready"  # "ready" means you can't see the bullet on the screen

# Explosion
explosion = pygame.image.load('icons/explode.png')
explosion_time = 0
explosion_position = (0, 0)  # Store the explosion position

# Replay button
replay_button_img = pygame.image.load('icons\Repeat__1_-removebg-preview.png')
replay_button_rect = replay_button_img.get_rect(center=(400, 350))  # Center the button

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over variables
game_over = False
game_over_sound_played = False  # Flag to check if game over sound has been played
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Function to display the score on the screen
def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Function to draw the player at the specified coordinates
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to draw the enemy at the specified coordinates
def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Function to fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Collision detection function
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Function to show the explosion
def show_explosion(x, y):
    screen.blit(explosion, (x, y))

# Function to display "Game Over"
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

# Function to reset the game state
def reset_game():
    global playerX, playerY, playerX_change, playerY_change, enemy_positions, enemy_x_change, bulletX, bulletY, bullet_state, score_value, game_over, game_over_sound_played, explosion_time, explosion_position, num_of_enemies

    # Reset player position
    playerX = 370
    playerY = 480
    playerX_change = 0
    playerY_change = 0

    # Reset enemy positions and speed
    enemy_positions = []
    enemy_x_change = []
    num_of_enemies = random.randint(1, 6)
    for i in range(num_of_enemies):
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)
        enemy_positions.append([enemyX, enemyY])
        enemy_x_change.append(0.5)

    # Reset bullet
    bulletX = 0
    bulletY = playerY
    bullet_state = "ready"

    # Reset score
    score_value = 0

    # Reset game over state
    game_over = False
    game_over_sound_played = False
    explosion_time = 0
    explosion_position = (0, 0)

    # Restart background music
    mixer.music.play(-1)

# Game loop
running = True
while running:

    # Fill the screen with a color
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checking for left/right/up/down keystrokes
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.5
                if event.key == pygame.K_UP:
                    playerY_change = -0.5
                if event.key == pygame.K_DOWN:
                    playerY_change = 0.5

            # Checking for key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        # Check if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                mouse_pos = pygame.mouse.get_pos()
                if replay_button_rect.collidepoint(mouse_pos):
                    reset_game()

    # Continuous fire logic
    keys = pygame.key.get_pressed()
    if not game_over and keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_sound = mixer.Sound('Sounds/mario_jump.mp3')
        bullet_sound.play()
        bulletX = playerX
        bulletY = playerY
        fire_bullet(bulletX, bulletY)

    # Update the player position
    if not game_over:
        playerX += playerX_change
        playerY += playerY_change

    # Defining boundaries of the player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 540:
        playerY = 540

    # Enemy movement logic (horizontal and then vertical)
    for i in range(num_of_enemies):
        if not game_over:
            enemy_positions[i][0] += enemy_x_change[i]

        # Check if the enemy hits the edge
        if enemy_positions[i][0] <= 0:
            enemy_x_change[i] = 0.3  # Move right
            if not game_over:
                enemy_positions[i][1] += enemy_y_change  # Move down
        elif enemy_positions[i][0] >= 736:
            enemy_x_change[i] = -0.3  # Move left
            if not game_over:
                enemy_positions[i][1] += enemy_y_change  # Move down

        # Check if enemy reaches the bottom (Game Over condition)
        if enemy_positions[i][1] >= 600:
            game_over = True
            mixer.music.stop()  # Stop background music
            break

        # Collision detection
        collision = is_collision(enemy_positions[i][0], enemy_positions[i][1], bulletX, bulletY)
        if collision:
            show_explosion(enemy_positions[i][0], enemy_positions[i][1])  # Show explosion at enemy's location
            pygame.display.update()
            explosion_time = pygame.time.get_ticks()  # Record the time when explosion starts
            explosion_position = (enemy_positions[i][0], enemy_positions[i][1])  # Record the explosion position

            bulletY = playerY  # Reset bullet to the player's Y position
            bullet_state = "ready"
            score_value += 1
            print(score_value)

            # Reset enemy position after collision
            enemy_positions[i][0] = random.randint(0, 736)
            enemy_positions[i][1] = random.randint(50, 150)

        # Draw each enemy on the screen
        if not game_over:
            enemy(enemy_positions[i][0], enemy_positions[i][1])

    # Bullet Movement
    if not game_over and bulletY <= 0:
        bulletY = playerY  # Reset bullet to the player's Y position
        bullet_state = "ready"

    if not game_over and bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Draw the player on the screen
    if not game_over:
        player(playerX, playerY)

    # Show score
    show_score(textX, textY)

    # Show "Game Over" message if the game is over
    if game_over:
        game_over_text()
        # Draw the replay button
        screen.blit(replay_button_img, replay_button_rect)
        # Play "Game Over" sound only once
        if not game_over_sound_played:
            game_over_sound = mixer.Sound('Sounds/mario_bros_die.mp3')
            game_over_sound.play()
            game_over_sound_played = True  # Set flag to True to prevent replay

    # Display the explosion for 0.6 seconds
    if explosion_time != 0 and pygame.time.get_ticks() - explosion_time < 350:
        bullet_sound = mixer.Sound('Sounds/mario_bros_coin.mp3')
        bullet_sound.play()
        show_explosion(*explosion_position)
    else:
        explosion_time = 0  # Reset explosion time

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
