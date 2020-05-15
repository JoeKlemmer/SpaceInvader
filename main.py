import pygame
import random
import time
import math

# Initialize pygame engine
pygame.init()

# Set the window size
size = width, height = 1024, 768
# size = width, height = 800, 600

# Create the screen (window)
screen = pygame.display.set_mode(size)

# Background image https://www.freepik.com/free-photos-vectors/background by rawpwww.freepik.com
if width == 800:
    background = pygame.image.load("background-902x600.jpg")
else:
    background = pygame.image.load("background-1154x768.jpg")

# Set the clock speed delta
clock = pygame.time.Clock()

score = 0
shots_fired = 0


# Quit event
# looking for the escape key pressed or the X close window button clicked
def quitting(event):
    escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    x_button = event.type == pygame.QUIT
    return x_button or escape


# Set title and icon (image made by Freepik <https://www.flaticon.com/authors/freepik>, Downloaded from www.flaticon.com)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Set playerImg (image made by Freepik <https://www.flaticon.com>, Downloaded from www.flaticon.com)
playerImg = pygame.image.load("player.png")
playerX = int((width / 2) - 32)
playerY = int(height * 0.85)
playerX_change = 0

# Set enemyImg <https://icons8.com/icons/set/planet-globe"> UFO icon by icons8.com
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, (height - 64))
enemyY = random.randint(0, (int(height * 0.10)))
enemyX_change = 4
enemyY_change = 40

# Bullet Icon made by Those Icons https://www.flaticon.com/authors/those-icons> from www.flaticon.com
# State of 'ready' is waiting
# State of 'fired' is in motion
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = int(height * 0.85)
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


# Display player
def player(x, y):
    screen.blit(playerImg, (x, y))


# Display enemy
def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# Fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


# Main game loop
running = True

while running:
    for event in pygame.event.get():
        if quitting(event):
            running = False

        # Move the player on the X-axis with the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    shots_fired += 1
                    print("Shots fired: " + str(shots_fired))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_change = 0

    # Set RGB values for background
    screen.fill((0, 0, 0))
    # Load bg image
    screen.blit(background, (0, 0))

    # Player movement
    playerX += playerX_change

    # Keep the players X-axis from going off the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= width - 64:
        playerX = width - 64

    enemyX += enemyX_change

    # Keep the enemys X-axis from going off the screen
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= width - 64:
        enemyX_change = -4
        enemyY += enemyY_change

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = int(height * 0.85)

    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Test for collsion
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = int(height * 0.85)
        bullet_state = "ready"
        score += 1
        print("Your score: " + str(score))
        enemyX = random.randint(0, (height - 64))
        enemyY = random.randint(0, 150)

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    # Update the screen
    pygame.display.update()
    clock.tick(60)

print("Hit percentage is: " + str((score / shots_fired) * 100) + "%")
