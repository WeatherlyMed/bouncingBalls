import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball with Magnetic Effect and Tilting Line")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
ball_color = (0, 0, 255)  # Blue ball

# Define initial properties
line_thickness = 10
max_slope = 0.45  # Increased tilt slope (45%) - 3 times original
tilt_duration = 10  # Duration of each tilt in seconds
pause_duration = 10  # Duration of pause between tilts in seconds

# Ball properties
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_velocity = [3, 3]  # Initial velocity
gravity = 0.5
magnet_strength = 4.0  # Increased magnetic acceleration strength (4x original)
energy_loss_factor = 0.3  # 70% energy loss

def draw_tilting_line(time_elapsed):
    # Calculate the current slope based on the time elapsed
    total_cycle_time = 2 * tilt_duration + pause_duration
    cycle_position = time_elapsed % total_cycle_time
    slope = 0
    
    if cycle_position < tilt_duration:
        # Increasing slope
        slope = (max_slope * cycle_position) / tilt_duration
    elif cycle_position < tilt_duration + pause_duration:
        # Pause
        slope = max_slope
    else:
        # Decreasing slope
        time_in_decreasing_slope = cycle_position - (tilt_duration + pause_duration)
        slope = max_slope * (1 - time_in_decreasing_slope / tilt_duration)
    
    # Line coordinates with dynamic slope
    line_start_x = 0
    line_start_y = height - line_thickness
    line_end_x = width
    line_end_y = height - line_thickness - slope * width
    
    if line_end_y < 0:
        line_end_y = 0
        slope = (height - line_thickness) / width
    
    pygame.draw.line(screen, white, (line_start_x, line_start_y), (line_end_x, line_end_y), line_thickness)
    
    return (line_start_x, line_start_y, line_end_x, line_end_y, slope, line_end_y)

def apply_magnetic_effect(ball_x, ball_y):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Only apply magnetic effect if mouse is within window
    if 0 <= mouse_x <= width and 0 <= mouse_y <= height:
        dx = mouse_x - ball_x
        dy = mouse_y - ball_y
        distance = math.hypot(dx, dy)
        if distance < width // 2:  # Use window width/2 as the distance threshold
            magnetic_force = magnet_strength * (1 - distance / (width // 2))
            angle = math.atan2(dy, dx)
            ball_velocity[0] += magnetic_force * math.cos(angle)
            ball_velocity[1] += magnetic_force * math.sin(angle)

def update_ball(line_coords):
    global ball_x, ball_y, ball_velocity
    
    # Update ball position based on velocity
    ball_x += ball_velocity[0]
    ball_y += ball_velocity[1]
    
    # Apply gravity
    ball_velocity[1] += gravity
    
    # Bounce off the walls
    if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
        ball_velocity[0] = -ball_velocity[0] * energy_loss_factor
    if ball_y - ball_radius < 0:
        ball_velocity[1] = -ball_velocity[1] * energy_loss_factor
    
    # Ensure the ball stays within bounds
    ball_x = max(ball_radius, min(ball_x, width - ball_radius))
    ball_y = max(ball_radius, min(ball_y, height - ball_radius))
    
    # Bounce off the tilting line
    (line_start_x, line_start_y, line_end_x, line_end_y, slope, line_y) = line_coords
    intercept = line_start_y - slope * line_start_x
    
    line_y_at_ball_x = slope * ball_x + intercept
    
    if ball_y + ball_radius > line_y_at_ball_x:
        ball_y = line_y_at_ball_x - ball_radius
        normal = (-slope, 1)
        norm_length = math.hypot(normal[0], normal[1])
        normal = (normal[0] / norm_length, normal[1] / norm_length)
        dot_product = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]
        ball_velocity[0] -= 2 * dot_product * normal[0] * energy_loss_factor
        ball_velocity[1] -= 2 * dot_product * normal[1] * energy_loss_factor
    
    # Ensure ball does not go below the line (hard barrier)
    if ball_y + ball_radius > line_y:
        ball_y = line_y - ball_radius
        ball_velocity[1] = -ball_velocity[1] * energy_loss_factor  # Bounce back

def main():
    global running
    running = True
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time_elapsed = time.time() - start_time

        # Clear the screen
        screen.fill(black)
        
        # Draw the tilting line and get its coordinates
        line_coords = draw_tilting_line(time_elapsed)
        
        # Apply magnetic effect to the ball
        apply_magnetic_effect(ball_x, ball_y)
        
        # Update ball position and handle collision with the tilting line
        update_ball(line_coords)
        
        # Draw the ball
        pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)
        
        # Update the display
        pygame.display.flip()

        # Delay to control frame rate
        pygame.time.delay(30)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
