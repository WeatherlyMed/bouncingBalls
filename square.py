import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Square Simulation")

# Colors
black = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

# Initial properties of the bouncing square
square_size = 50
square_x, square_y = width // 2 - square_size // 2, height // 2 - square_size // 2

# Generate a random angle for the initial velocity
angle = random.uniform(0, 2 * math.pi)
speed = 5
velocity = [speed * math.cos(angle), speed * math.sin(angle)]

current_color = random.choice(colors)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the square
    square_x += velocity[0]
    square_y += velocity[1]

    # Bounce off the edges and change size and color
    if square_x <= 0 or square_x + square_size >= width:
        velocity[0] = -velocity[0]
        square_x += velocity[0]
        square_size += 10
        current_color = random.choice(colors)
    if square_y <= 0 or square_y + square_size >= height:
        velocity[1] = -velocity[1]
        square_y += velocity[1]
        square_size += 10
        current_color = random.choice(colors)

    # Ensure the square doesn't go out of bounds
    if square_x < 0:
        square_x = 0
    if square_x + square_size > width:
        square_x = width - square_size
    if square_y < 0:
        square_y = 0
    if square_y + square_size > height:
        square_y = height - square_size

    # Stop the simulation if the square fills the screen
    if square_size >= width or square_size >= height:
        running = False

    # Clear the screen
    screen.fill(black)
    
    # Draw the square
    pygame.draw.rect(screen, current_color, (square_x, square_y, square_size, square_size))
    
    # Update the display
    pygame.display.flip()

    # Delay to control frame rate
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
