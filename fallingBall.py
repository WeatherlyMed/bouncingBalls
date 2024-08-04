import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Falling Ball')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ball properties
ball_radius = 20
ball_x = width // 2
ball_y = ball_radius
ball_color = BLACK
ball_speed_x = 0
ball_speed_y = 0
gravity = 0.5

# Circle properties
circle_radius = 100
circle_x = width // 2
circle_y = height // 2
circle_color = WHITE

# Clock object to control frame rate
clock = pygame.time.Clock()

# Universal bounce function
def bounce(obj_x, obj_y, obj_radius, surface_x, surface_y, surface_radius, speed_x, speed_y):
    dx = obj_x - surface_x
    dy = obj_y - surface_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance < surface_radius - obj_radius:
        speed_y = -speed_y  # Bounce off the surface
        speed_x = -speed_x  # Bounce off the surface
    return speed_x, speed_y

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_speed_y += gravity
    ball_y += ball_speed_y
    ball_x += ball_speed_x

    # Check if the ball hits the ground
    if ball_y >= height - ball_radius:
        ball_y = height - ball_radius
        ball_speed_y, ball_speed_x = bounce(ball_x, ball_y, ball_radius, ball_x, height - ball_radius, ball_radius, ball_speed_x, ball_speed_y)

    # Check if the ball hits the left or right wall
    if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
        ball_speed_x = -ball_speed_x

    # Check if the ball is inside the circle
    ball_speed_y, ball_speed_x = bounce(ball_x, ball_y, ball_radius, circle_x, circle_y, circle_radius, ball_speed_x, ball_speed_y)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the circle
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()()
