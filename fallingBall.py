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
ball_color = BLACK
ball_speed_x = 0
ball_speed_y = 0
gravity = 0.2

# Circle properties
circle_radius = 100
circle_x = width // 2
circle_y = height // 2
circle_color = BLACK
hole_radius = 30
hole_angle = 0
angle_speed = 1

# Ensure the ball starts within the circle
def random_position_within_circle(center_x, center_y, radius, ball_radius):
    angle = math.radians(hole_angle)
    distance = radius - ball_radius - 1  # Ensuring it fits inside the circle
    x = center_x + distance * math.cos(angle)
    y = center_y + distance * math.sin(angle)
    return x, y

ball_x, ball_y = random_position_within_circle(circle_x, circle_y, circle_radius, ball_radius)

# Clock object to control frame rate
clock = pygame.time.Clock()

# Universal bounce function with energy loss
def bounce(obj_x, obj_y, obj_radius, surface_x, surface_y, surface_radius, speed_x, speed_y, energy_loss=0.9):
    dx = obj_x - surface_x
    dy = obj_y - surface_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance < surface_radius - obj_radius:
        # Calculate the normal
        normal_x = dx / distance
        normal_y = dy / distance
        # Reflect the velocity
        dot_product = speed_x * normal_x + speed_y * normal_y
        speed_x -= 2 * dot_product * normal_x
        speed_y -= 2 * dot_product * normal_y
        # Apply energy loss
        speed_x *= energy_loss
        speed_y *= energy_loss
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

    # Check if the ball is inside the circle or goes through the hole
    dx = ball_x - circle_x
    dy = ball_y - circle_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance < circle_radius - ball_radius:
        if distance < circle_radius - hole_radius:
            hole_x = circle_x + math.cos(math.radians(hole_angle)) * (circle_radius - hole_radius)
            hole_y = circle_y + math.sin(math.radians(hole_angle)) * (circle_radius - hole_radius)
            if math.hypot(ball_x - hole_x, ball_y - hole_y) > hole_radius:
                ball_speed_x, ball_speed_y = bounce(ball_x, ball_y, ball_radius, circle_x, circle_y, circle_radius, ball_speed_x, ball_speed_y, energy_loss=0.9)
            else:
                running = False  # Ball goes through the hole, end the simulation
        else:
            ball_speed_x, ball_speed_y = bounce(ball_x, ball_y, ball_radius, circle_x, circle_y, circle_radius, ball_speed_x, ball_speed_y, energy_loss=0.9)
    else:
        # Adjust position if ball is outside the circle (for robustness)
        ball_x = circle_x + (circle_radius - ball_radius) * (dx / distance)
        ball_y = circle_y + (circle_radius - ball_radius) * (dy / distance)
        ball_speed_x, ball_speed_y = bounce(ball_x, ball_y, ball_radius, circle_x, circle_y, circle_radius, ball_speed_x, ball_speed_y, energy_loss=0.9)

    # Rotate the circle
    hole_angle += angle_speed

    # Clear the screen
    screen.fill(WHITE)

    # Draw the circle and hole
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius, 2)
    hole_x = circle_x + math.cos(math.radians(hole_angle)) * (circle_radius - hole_radius)
    hole_y = circle_y + math.sin(math.radians(hole_angle)) * (circle_radius - hole_radius)
    pygame.draw.circle(screen, WHITE, (int(hole_x), int(hole_y)), hole_radius)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Draw the outside barrier
    pygame.draw.rect(screen, BLACK, (0, 0, width, 20))  # Top
    pygame.draw.rect(screen, BLACK, (0, 0, 20, height))  # Left
    pygame.draw.rect(screen, BLACK, (width - 20, 0, 20, height))  # Right
    pygame.draw.rect(screen, BLACK, (0, height - 20, width, 20))  # Bottom

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
