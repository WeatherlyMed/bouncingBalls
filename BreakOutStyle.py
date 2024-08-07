import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout with Tilting Line")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
colors = [red, green, blue, yellow, cyan, magenta]

# Define constants
square_size = 20
ball_radius = square_size // 2
base_speed = 15
speed = base_speed
angle = random.uniform(0, 2 * math.pi)
velocity = [speed * math.cos(angle), speed * math.sin(angle)]
magnetic_effect_distance = 150
magnetic_acceleration = 0.3
gravity = 0.5
energy_loss_factor = 0.8  # Energy loss factor on bounce (1.0 means no loss, <1.0 means loss)

# Create blocks
block_width = 60 * 1.3
block_height = 30
block_gap = square_size + 4
block_row_gap = block_height * 0.6
blocks = []
new_row_timer = time.time()
row_interval = 10
scroll_speed = 0.25
hits_required = 1

# Point counter
points = 0
points_timer = time.time()
points_interval = 1

# Ball properties
balls = [{'x': width // 2 - ball_radius, 'y': height // 2 - ball_radius, 'size': square_size, 'velocity': velocity, 'color': white}]

# Particle system
particles = []

def create_particles(x, y, color):
    for _ in range(50):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        particle = {'x': x, 'y': y, 'velocity': velocity, 'color': color, 'lifetime': random.uniform(0.5, 1.0)}
        particles.append(particle)

def update_particles():
    for particle in particles[:]:
        particle['x'] += particle['velocity'][0]
        particle['y'] += particle['velocity'][1]
        particle['lifetime'] -= 0.02
        if particle['lifetime'] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        alpha = int(255 * particle['lifetime'])
        color = (*particle['color'][:3], alpha)
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        s.fill(color)
        screen.blit(s, (particle['x'], particle['y']))

def draw_block(block):
    pygame.draw.rect(screen, block['color'], (block['x'], block['y'], block['width'], block['height']))

def update_balls():
    for ball in balls:
        # Update ball position
        ball['x'] += ball['velocity'][0]
        ball['y'] += ball['velocity'][1]

        # Check for collisions with blocks
        for block in blocks[:]:
            if (
                ball['x'] + ball['size'] >= block['x'] and
                ball['x'] <= block['x'] + block['width'] and
                ball['y'] + ball['size'] >= block['y'] and
                ball['y'] <= block['y'] + block['height']
            ):
                # Bounce off the block
                if ball['x'] + ball['size'] - ball['velocity'][0] <= block['x'] or \
                   ball['x'] - ball['velocity'][0] >= block['x'] + block['width']:
                    ball['velocity'][0] = -ball['velocity'][0]
                else:
                    ball['velocity'][1] = -ball['velocity'][1]

                # Apply energy loss
                ball['velocity'][0] *= energy_loss_factor
                ball['velocity'][1] *= energy_loss_factor

                create_particles(ball['x'] + ball['size'] // 2, 
                                 ball['y'] + ball['size'] // 2, block['color'])
                block['hits'] -= 1
                if block['hits'] <= 0:
                    blocks.remove(block)

        # Bounce off the edges of the screen
        if ball['x'] <= 0 or ball['x'] + ball['size'] >= width:
            ball['velocity'][0] = -ball['velocity'][0]
            # Apply energy loss
            ball['velocity'][0] *= energy_loss_factor
        if ball['y'] <= 0:
            ball['velocity'][1] = -ball['velocity'][1]
            # Apply energy loss
            ball['velocity'][1] *= energy_loss_factor
        if ball['y'] + ball['size'] >= height:
            ball['y'] = height - ball['size']
            ball['velocity'][1] = -ball['velocity'][1]
            # Apply energy loss
            ball['velocity'][1] *= energy_loss_factor

    return True

def update_blocks():
    global new_row_timer, scroll_speed
    current_time = time.time()
    if current_time - new_row_timer > row_interval:
        new_blocks = create_block_row(-block_height)
        blocks.extend(new_blocks)
        scroll_speed *= 1.05
        new_row_timer = current_time

    for block in blocks[:]:
        block['y'] += scroll_speed
        if block['y'] + block['height'] >= height:
            return False

    return True

def update_points():
    global points, points_timer
    current_time = time.time()
    if current_time - points_timer >= points_interval:
        points += 10
        points_timer = current_time

def create_block_row(y_offset=0):
    row_blocks = []
    block_cols = int((width - 20) // (block_width + block_gap))
    for col in range(block_cols):
        x = col * (block_width + block_gap) + 10
        y = y_offset
        color = colors[col % len(colors)]
        row_blocks.append({'x': x, 'y': y, 'width': block_width, 'height': block_height, 'color': color, 'hits': hits_required})
    return row_blocks

def draw_tilting_line(angle):
    line_length = width
    base_line_height = height - 50
    max_tilt_height = 50
    
    line_angle = angle
    line_height_left = base_line_height - max_tilt_height * math.sin(line_angle)
    line_height_right = base_line_height + max_tilt_height * math.cos(line_angle)
    
    line_x1 = 0
    line_y1 = line_height_left
    line_x2 = width
    line_y2 = line_height_right
    
    pygame.draw.line(screen, white, (line_x1, line_y1), (line_x2, line_y2), 5)

    return line_x1, line_y1, line_x2, line_y2

def apply_magnetic_effect():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for ball in balls:
        ball_center_x = ball['x'] + ball_radius
        ball_center_y = ball['y'] + ball_radius
        dx = mouse_x - ball_center_x
        dy = mouse_y - ball_center_y
        distance = math.hypot(dx, dy)
        
        if distance < magnetic_effect_distance:
            force_magnitude = magnetic_acceleration * (1 - distance / magnetic_effect_distance)
            angle_to_cursor = math.atan2(dy, dx)
            ball['velocity'][0] += force_magnitude * math.cos(angle_to_cursor)
            ball['velocity'][1] += force_magnitude * math.sin(angle_to_cursor)

def main():
    global running, new_row_timer, points_timer, level_start_time

    running = True
    new_row_timer = time.time()
    points_timer = time.time()
    level_start_time = time.time()

    # Initialize blocks with one row
    blocks.extend(create_block_row(0))

    # Initial angle for the tilting line
    line_angle = 0
    angle_velocity = 0.02

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_balls()
        apply_magnetic_effect()
        update_particles()
        running = update_blocks()
        update_points()

        # Update the tilting line angle
        line_angle += angle_velocity
        if line_angle > 2 * math.pi:
            line_angle -= 2 * math.pi

        # Clear the screen
        screen.fill(black)

        # Draw the blocks
        for block in blocks:
            draw_block(block)

        # Draw the balls
        for ball in balls:
            pygame.draw.circle(screen, ball['color'], 
                               (int(ball['x'] + ball_radius), 
                                int(ball['y'] + ball_radius)), 
                               ball_radius)

        # Draw the tilting line
        draw_tilting_line(line_angle)

        # Draw particles
        draw_particles()

        # Draw the point counter
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Points: {points}', True, white)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        pygame.time.delay(16)

    pygame.quit()

if __name__ == "__main__":
    main()
