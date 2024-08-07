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
base_speed = 15  # Increased base speed by 3 times
speed = base_speed * 2  # Increased speed by 2 times
angle = random.uniform(0, 2 * math.pi)
velocity = [speed * math.cos(angle), speed * math.sin(angle)]

# Create blocks
block_width = 60 * 1.3  # Increased block width by 30%
block_height = 30
block_gap = square_size + 4  # Gap between columns 4 pixels larger than the ball
block_row_gap = block_height * 0.6  # Decreased the gap between rows by 40%
blocks = []
new_row_timer = time.time()
row_interval = 10  # Time in seconds to spawn a new row of blocks
scroll_speed = 0.25  # Initial scroll speed factor (reduced by 50%)
hits_required = 1  # Initial hits required to destroy a block

# Point counter
points = 0
points_timer = time.time()
points_interval = 1  # Time in seconds to increase points

# Ball properties
balls = [{'x': width // 2 - square_size // 2, 'y': height // 2 - square_size // 2, 'size': square_size, 'velocity': velocity, 'color': white}]

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

def update_balls():
    for ball in balls:
        ball['x'] += ball['velocity'][0]
        ball['y'] += ball['velocity'][1]

        # Check for collisions with the blocks
        for block in blocks[:]:
            if (
                ball['x'] + ball['size'] >= block['x'] and
                ball['x'] <= block['x'] + block['width'] and
                ball['y'] + ball['size'] >= block['y'] and
                ball['y'] <= block['y'] + block['height']
            ):
                if ball['x'] + ball['size'] - ball['velocity'][0] <= block['x'] or \
                   ball['x'] - ball['velocity'][0] >= block['x'] + block['width']:
                    ball['velocity'][0] = -ball['velocity'][0]
                else:
                    ball['velocity'][1] = -ball['velocity'][1]
                
                create_particles(ball['x'] + ball['size'] // 2, 
                                 ball['y'] + ball['size'] // 2, block['color'])
                block['hits'] -= 1
                if block['hits'] <= 0:
                    blocks.remove(block)

        # Bounce off the edges of the screen
        if ball['x'] <= 0 or ball['x'] + ball['size'] >= width:
            ball['velocity'][0] = -ball['velocity'][0]
        if ball['y'] <= 0:
            ball['velocity'][1] = -ball['velocity'][1]
        if ball['y'] + ball['size'] >= height:  # Ball reaches the bottom
            ball['y'] = height - ball['size']  # Reset position to bottom
            ball['velocity'][1] = -ball['velocity'][1]  # Bounce back up
    return True

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

def create_block_row(y_offset=0):
    row_blocks = []
    block_cols = int((width - 20) // (block_width + block_gap))  # Number of blocks that fit within the screen width
    for col in range(block_cols):
        x = col * (block_width + block_gap) + 10  # Added space from left edge
        y = y_offset
        color = colors[col % len(colors)]
        row_blocks.append({'x': x, 'y': y, 'width': block_width, 'height': block_height, 'color': color, 'hits': hits_required})
    return row_blocks

def start_new_level():
    global speed, hits_required, level_start_time, balls
    speed *= 1.5  # Increase speed by 50%
    hits_required += 1  # Increase hits required for blocks by 1
    level_start_time = time.time()  # Reset level start time
    
    # Update ball velocities
    for ball in balls:
        angle = random.uniform(0, 2 * math.pi)
        ball['velocity'] = [speed * math.cos(angle), speed * math.sin(angle)]

def display_level_screen():
    screen.fill(black)
    font = pygame.font.Font(None, 74)
    
    level_text = font.render(f"Level {hits_required - 1}", True, white)
    lives_text = font.render(f"Lives: {hits_required}", True, white)
    speed_text = font.render(f"Speed Boost: {speed / base_speed:.2f}x", True, white)
    
    screen.blit(level_text, (width // 2 - level_text.get_width() // 2, height // 2 - 100))
    screen.blit(lives_text, (width // 2 - lives_text.get_width() // 2, height // 2))
    screen.blit(speed_text, (width // 2 - speed_text.get_width() // 2, height // 2 + 100))
    
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before continuing

# Main game loop
def main():
    global running, new_row_timer, points_timer, level_start_time
    running = True
    new_row_timer = time.time()
    points_timer = time.time()
    level_start_time = time.time()
    
    # Initialize blocks with one row
    blocks.extend(create_block_row(0))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not update_balls():
            running = False
        
        update_particles()
        running = update_blocks()
        update_points()

        # Check if it's time to start a new level
        current_time = time.time()
        if current_time - level_start_time >= 60:
            display_level_screen()
            start_new_level()

        # Clear the screen
        screen.fill(black)

        # Draw the blocks
        for block in blocks:
            draw_block(block)

        # Draw the balls
        for ball in balls:
            pygame.draw.rect(screen, ball['color'], 
                             (ball['x'], ball['y'], 
                              ball['size'], ball['size']))

        # Draw particles
        draw_particles()

        # Draw the point counter
        font = pygame.font.Font(None, 36)
        text = font.render(f"Points: {points}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Delay to control frame rate
        pygame.time.delay(16)  # Approximately 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
