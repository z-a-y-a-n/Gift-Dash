import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gift Dash")

# Load assets
background = pygame.image.load("background.jpg")
player_image = pygame.image.load("hand.png")
gift_box_image = pygame.image.load("giftbox.png")
capture_sound = pygame.mixer.Sound("sound.wav")
lost_sound = pygame.mixer.Sound("lost.wav")
score_sound = pygame.mixer.Sound("score.wav")

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Scale assets
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.transform.scale(player_image, (50, 50))
gift_box_image = pygame.transform.scale(gift_box_image, (50, 50))

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Player properties
player_x = SCREEN_WIDTH // 2 - player_image.get_width() // 2
player_y = SCREEN_HEIGHT - player_image.get_height() - 10
player_speed = 4.1

# Gift box properties
gift_box_x = random.randint(0, SCREEN_WIDTH - gift_box_image.get_width())
gift_box_y = 0
gift_box_speed = 3.5
current_speed_level = 1

# Score
score = 0
score_font = pygame.font.Font(None, 36)

# Gradient colors
start_color = RED
end_color = YELLOW

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Update player position
    if player_x < 0:
        player_x = 0
    elif player_x > SCREEN_WIDTH - player_image.get_width():
        player_x = SCREEN_WIDTH - player_image.get_width()

    # Update gift box position
    gift_box_y += gift_box_speed

    # Check if the player captures the gift box
    if (
        gift_box_y + gift_box_image.get_height() >= player_y
        and gift_box_x + gift_box_image.get_width() >= player_x
        and gift_box_x <= player_x + player_image.get_width()
    ):
        # Increase the score, play capture sound, and reset the gift box position
        score += 1
        capture_sound.play()
        gift_box_x = random.randint(0, SCREEN_WIDTH - gift_box_image.get_width())
        gift_box_y = 0

        # Increase speed every 10 points
        if score % 5 == 0:
            current_speed_level += 1
            gift_box_speed += 1
            player_speed += 0.5
        
        #Play score sound if the score is equal to 3
        if score == 3:
            score_sound.play()

    # Check if the gift box reaches the bottom of the screen
    if gift_box_y > SCREEN_HEIGHT:
        # Reset the gift box position
        gift_box_x = random.randint(0, SCREEN_WIDTH - gift_box_image.get_width())
        gift_box_y = 0

        # Set missed_box to True and end the game
        missed_box = True
        break

    # Draw the background
    screen.blit(background, (0, 1))

    # Draw the player and gift box
    screen.blit(player_image, (player_x, player_y))
    screen.blit(gift_box_image, (gift_box_x, gift_box_y))

    # Draw the score with gradient color
    score_text = score_font.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

if missed_box:
    # Display "You lost" message in red color
    font_lost = pygame.font.Font(None, 72)
    lost_sound.play()
    lost_text = font_lost.render("You lost!", True, RED)
    screen.blit(
        lost_text,
        (SCREEN_WIDTH // 2 - lost_text.get_width() // 2, SCREEN_HEIGHT // 2 - lost_text.get_height() // 2),
    )
    pygame.display.flip()
    pygame.time.delay(2000)  # Display the message for 2 seconds

pygame.quit()
