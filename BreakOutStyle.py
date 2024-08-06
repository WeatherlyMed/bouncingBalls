import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Simulation")

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

# Define initial properties
square_size = 20
base_speed = 5
speed = base_speed * 6  # Increased speed by 6 times (2 times the previously increased speed)
angle = random.uniform(0, 2 * math.pi)
velocity = [speed * math.cos(angle), speed * math.sin(angle)]

# Create blocks
block_cols = 10
block_gap = 5
block_width = (width - (block_gap * (block_cols - 1)) - 40) // block_cols  # Adjusted for edge space
block_height = 30
block_row_gap = block_height * 0.6  # Decreased the gap between rows by 40%
blocks = []
new_row_timer = 0
row_interval = 5  # Time in seconds to spawn a new row of blocks
scroll_speed = 0.5  # Initial scroll speed factor (reduced by 50%)

# Point counter
points = 0
points_timer = 0
points_interval = 1  # Time in seconds to increase points

def create_block_row(y_offset=0):
    row_blocks = []
    for col in range(block_cols):
        x = col * (block_width + block_gap) + 20  # Added space from left edge
        y = y_offset
        color = colors[col % len(colors)]
        row_blocks.append({'x': x, 'y': y, 'width': block_width, 'height': block_height, 'color': color})
    return row_blocks

# Initial blocks
blocks.extend(create_block_row())

# Small bouncing square
bouncing_square = {'x': width // 2, 'y': height // 2, 'size': square_size, 'velocity': velocity, 'color': white}

# Particle system
particles = []

def create_particles(x, y, color):
    for _ in range(50):  # Number of particles
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        particle = {'x': x, 'y': y, 'velocity': velocity, 'color': color, 'lifetime': random.uniform(0.5, 1.0)}
        particles.append(particle)

def update_particles():
    for particle in particles[:]:
        particle['x'] += particle['velocity'][0]
        particle['y'] += particle['velocity'][1]
        particle['lifetime'] -= 0.02  # Fade out effect
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

def update_bouncing_square():
    bouncing_square['x'] += bouncing_square['velocity'][0]
    bouncing_square['y'] += bouncing_square['velocity'][1]

    # Check for collisions with the blocks
    for block in blocks[:]:
        if (
            bouncing_square['x'] + bouncing_square['size'] >= block['x'] and
            bouncing_square['x'] <= block['x'] + block['width'] and
            bouncing_square['y'] + bouncing_square['size'] >= block['y'] and
            bouncing_square['y'] <= block['y'] + block['height']
        ):
            if bouncing_square['x'] + bouncing_square['size'] - bouncing_square['velocity'][0] <= block['x'] or \
               bouncing_square['x'] - bouncing_square['velocity'][0] >= block['x'] + block['width']:
                bouncing_square['velocity'][0] = -bouncing_square['velocity'][0]
            else:
                bouncing_square['velocity'][1] = -bouncing_square['velocity'][1]
            
            create_particles(bouncing_square['x'] + bouncing_square['size'] // 2, 
                             bouncing_square['y'] + bouncing_square['size'] // 2, block['color'])
            blocks.remove(block)

    # Bounce off the edges of the screen
    if bouncing_square['x'] <= 0 or bouncing_square['x'] + bouncing_square['size'] >= width:
        bouncing_square['velocity'][0] = -bouncing_square['velocity'][0]
    if bouncing_square['y'] <= 0 or bouncing_square['y'] + bouncing_square['size'] >= height:
        bouncing_square['velocity'][1] = -bouncing_square['velocity'][1]

    # Ensure the square doesn't go out of bounds
    if bouncing_square['x'] < 0:
        bouncing_square['x'] = 0
    if bouncing_square['x'] + bouncing_square['size'] > width:
        bouncing_square['x'] = width - bouncing_square['size']
    if bouncing_square['y'] < 0:
        bouncing_square['y'] = 0
    if bouncing_square['y'] + bouncing_square['size'] > height:
        bouncing_square['y'] = height - bouncing_square['size']

def update_blocks():
    global new_row_timer, scroll_speed
    current_time = time.time()
    if current_time - new_row_timer > row_interval:
        new_blocks = create_block_row(-block_height)
        blocks.extend(new_blocks)
        scroll_speed *= 1.05  # Increase scroll speed by 5%
        new_row_timer = current_time

    for block in blocks[:]:
        block['y'] += scroll_speed  # Move blocks down based on scroll speed
        if block['y'] + block['height'] >= height:
            return False  # End game if any block reaches the bottom

    return True

def update_points():
    global points, points_timer
    current_time = time.time()
    if current_time - points_timer >= points_interval:
        points += 10
        points_timer = current_time

def main():
    global running, new_row_timer, points_timer
    running = True
    new_row_timer = time.time()
    points_timer = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_bouncing_square()
        update_particles()
        running = update_blocks()
        update_points()

        # Clear the screen
        screen.fill(black)

        # Draw the blocks
        for block in blocks:
            draw_block(block)

        # Draw the bouncing square
        pygame.draw.rect(screen, bouncing_square['color'], 
                         (bouncing_square['x'], bouncing_square['y'], 
                          bouncing_square['size'], bouncing_square['size']))

        # Draw particles
        draw_particles()

        # Draw the point counter
        font = pygame.font.Font(None, 36)
        text = font.render(f"Points: {points}", True, white)
        screen.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Delay to control frame rate
        pygame.time.delay(30)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
