import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Square Simulation")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
color_names = {
    (255, 0, 0): "Red",
    (0, 255, 0): "Green",
    (0, 0, 255): "Blue",
    (255, 255, 0): "Yellow",
    (0, 255, 255): "Cyan",
    (255, 0, 255): "Magenta"
}
all_colors = list(color_names.keys())

# Define initial properties
square_size = 50
speed = 5  # Adjusted speed for better collision handling
angle = random.uniform(0, 2 * math.pi)
velocity = [speed * math.cos(angle), speed * math.sin(angle)]

# Shuffle colors to ensure random selection
random.shuffle(all_colors)
available_colors = all_colors.copy()

# Initial color is white for the original square
original_square_color = white
current_color = available_colors.pop()
current_color_name = color_names[current_color]

# List to store squares
squares = [{'x': width // 2 - square_size // 2, 'y': height // 2 - square_size // 2,
            'size': square_size, 'velocity': velocity, 'color': original_square_color, 'is_original': True, 'last_spawn_time': 0}]

spawn_delay = 2  # seconds

def draw_square(square):
    pygame.draw.rect(screen, square['color'], (square['x'], square['y'], square['size'], square['size']))

def display_color_name():
    font = pygame.font.Font(None, 36)
    text = font.render(current_color_name, True, (255, 255, 255))
    screen.blit(text, (10, 10))

def update_squares():
    global current_color, current_color_name, available_colors
    
    new_squares = []
    for square in squares:
        square['x'] += square['velocity'][0]
        square['y'] += square['velocity'][1]

        # Bounce off the edges and create a new square if it's the original square
        if square['x'] <= 0 or square['x'] + square['size'] >= width:
            square['velocity'][0] = -square['velocity'][0]
            if square['is_original'] and time.time() - square['last_spawn_time'] >= spawn_delay:
                new_squares.append(create_new_square(square))

        if square['y'] <= 0 or square['y'] + square['size'] >= height:
            square['velocity'][1] = -square['velocity'][1]
            if square['is_original'] and time.time() - square['last_spawn_time'] >= spawn_delay:
                new_squares.append(create_new_square(square))

        # Ensure the square doesn't go out of bounds
        if square['x'] < 0:
            square['x'] = 0
        if square['x'] + square['size'] > width:
            square['x'] = width - square['size']
        if square['y'] < 0:
            square['y'] = 0
        if square['y'] + square['size'] > height:
            square['y'] = height - square['size']

    # Handle collisions between squares
    new_squares.extend(handle_collisions())

    squares.extend(new_squares)

def create_new_square(square):
    global available_colors, current_color, current_color_name
    
    angle = random.uniform(0, 2 * math.pi)
    velocity = [speed * math.cos(angle), speed * math.sin(angle)]
    if not available_colors:
        available_colors = all_colors.copy()
    new_color = available_colors.pop()
    current_color_name = color_names[new_color]
    square['last_spawn_time'] = time.time()
    return {'x': square['x'], 'y': square['y'], 'size': square_size, 'velocity': velocity, 'color': new_color, 'is_original': False, 'last_spawn_time': 0}

def handle_collisions():
    new_squares = []
    for i, square1 in enumerate(squares):
        for j, square2 in enumerate(squares):
            if i >= j:
                continue
            if check_collision(square1, square2):
                resolve_collision(square1, square2)
                if square1['is_original'] and time.time() - square1['last_spawn_time'] >= spawn_delay:
                    new_squares.append(create_new_square(square1))
                if square2['is_original'] and time.time() - square2['last_spawn_time'] >= spawn_delay:
                    new_squares.append(create_new_square(square2))
    return new_squares

def check_collision(square1, square2):
    if (square1['x'] < square2['x'] + square2['size'] and
        square1['x'] + square1['size'] > square2['x'] and
        square1['y'] < square2['y'] + square2['size'] and
        square1['y'] + square1['size'] > square2['y']):
        return True
    return False

def resolve_collision(square1, square2):
    # Calculate the overlap in x and y directions
    overlap_x = min(square1['x'] + square1['size'], square2['x'] + square2['size']) - max(square1['x'], square2['x'])
    overlap_y = min(square1['y'] + square1['size'], square2['y'] + square2['size']) - max(square1['y'], square2['y'])

    # Separate the squares based on the smallest overlap
    if overlap_x < overlap_y:
        if square1['x'] < square2['x']:
            square1['x'] -= overlap_x / 2
            square2['x'] += overlap_x / 2
        else:
            square1['x'] += overlap_x / 2
            square2['x'] -= overlap_x / 2
        square1['velocity'][0] = -square1['velocity'][0]
        square2['velocity'][0] = -square2['velocity'][0]
    else:
        if square1['y'] < square2['y']:
            square1['y'] -= overlap_y / 2
            square2['y'] += overlap_y / 2
        else:
            square1['y'] += overlap_y / 2
            square2['y'] -= overlap_y / 2
        square1['velocity'][1] = -square1['velocity'][1]
        square2['velocity'][1] = -square2['velocity'][1]

def main():
    global running
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_squares()

        # Clear the screen
        screen.fill(black)
        
        # Draw the squares
        for square in squares:
            draw_square(square)
        
        # Draw the color name of the last created square
        display_color_name()
        
        # Update the display
        pygame.display.flip()

        # Delay to control frame rate
        pygame.time.delay(30)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
