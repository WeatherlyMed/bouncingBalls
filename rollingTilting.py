import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tilting Line with Ball")

# Ball properties
ball_radius = 15
ball_x = WIDTH // 2
ball_y = HEIGHT - 50 - ball_radius  # Initialize ball on the line
ball_velocity_x = 0
ball_velocity_y = 0
gravity = 0.5

# Line properties
line_length = WIDTH
base_line_height = HEIGHT - 50
angle_velocity = 0.02
max_tilt_height = 50  # Maximum height change

# Timing control
start_time = time.time()

# Run until the user asks to quit
running = True
while running:
    # Calculate time
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Tilting logic
    cycle_time = 20
    tilt_time = 5
    tilt_phase = (elapsed_time % cycle_time) / tilt_time

    if tilt_phase < 1:
        # Tilt right
        line_angle = angle_velocity * tilt_phase
        line_height_left = base_line_height - max_tilt_height * tilt_phase
        line_height_right = base_line_height
    elif tilt_phase < 2:
        # Return to center
        line_angle = angle_velocity * (2 - tilt_phase)
        line_height_left = base_line_height - max_tilt_height
        line_height_right = base_line_height + max_tilt_height * (tilt_phase - 1)
    elif tilt_phase < 3:
        # Tilt left
        line_angle = -angle_velocity * (tilt_phase - 2)
        line_height_left = base_line_height - max_tilt_height
        line_height_right = base_line_height + max_tilt_height * (tilt_phase - 2)
    else:
        # Return to center
        line_angle = -angle_velocity * (4 - tilt_phase)
        line_height_left = base_line_height - max_tilt_height * (4 - tilt_phase)
        line_height_right = base_line_height

    # Clear the screen
    screen.fill(BLACK)

    # Line coordinates
    line_x1 = WIDTH // 2 - line_length // 2
    line_y1 = line_height_left
    line_x2 = WIDTH // 2 + line_length // 2
    line_y2 = line_height_right

    # Rotate line around the center
    line_center_x = (line_x1 + line_x2) / 2
    line_center_y = (line_y1 + line_y2) / 2

    # Calculate the endpoints of the line after rotation
    line_x1_rot = line_center_x + (line_x1 - line_center_x) * math.cos(line_angle) - (line_y1 - line_center_y) * math.sin(line_angle)
    line_y1_rot = line_center_y + (line_x1 - line_center_x) * math.sin(line_angle) + (line_y1 - line_center_y) * math.cos(line_angle)
    line_x2_rot = line_center_x + (line_x2 - line_center_x) * math.cos(line_angle) - (line_y2 - line_center_y) * math.sin(line_angle)
    line_y2_rot = line_center_y + (line_x2 - line_center_x) * math.sin(line_angle) + (line_y2 - line_center_y) * math.cos(line_angle)

    # Calculate the angle of the line
    line_slope = (line_y2_rot - line_y1_rot) / (line_x2_rot - line_x1_rot)
    line_intercept = line_y1_rot - line_slope * line_x1_rot

    # Update ball position based on gravity
    ball_velocity_y += gravity
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Ensure ball stays above the line and calculate the line's normal vector
    expected_y = line_slope * ball_x + line_intercept
    if ball_y + ball_radius > expected_y:
        # Calculate the normal of the line
        normal_x = -line_slope
        normal_y = 1
        norm_length = math.sqrt(normal_x ** 2 + normal_y ** 2)
        normal_x /= norm_length
        normal_y /= norm_length

        # Calculate the gravitational force component perpendicular to the line
        gravity_component = gravity * normal_y

        # Calculate the rolling force
        rolling_force = gravity_component - (ball_velocity_x * normal_x + ball_velocity_y * normal_y)

        # Update ball velocity for rolling
        ball_velocity_x += rolling_force * normal_x
        ball_velocity_y += rolling_force * normal_y

        # Correct the ball's position
        overlap = ball_y + ball_radius - expected_y
        ball_y -= overlap

    # Draw the line
    pygame.draw.line(screen, WHITE, (int(line_x1_rot), int(line_y1_rot)), (int(line_x2_rot), int(line_y2_rot)), 5)

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
