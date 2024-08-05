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
square_x, square_y = width // 2 - square_size // 2, height // 2 - square_size // 2
speed = 10  # Increased speed
angle = random.uniform(0, 2 * math.pi)
velocity = [speed * math.cos(angle), speed * math.sin(angle)]

# Shuffle colors to ensure random selection
random.shuffle(all_colors)
available_colors = all_colors.copy()

current_color = available_colors.pop()
current_color_name = color_names[current_color]

# To store the last positions of the square
trail = []

def draw_trail(surface, trail):
    for i, (x, y, size, color) in enumerate(trail):
        # Calculate the distance from the current square to the trail square
        distance = math.sqrt((x - square_x) ** 2 + (y - square_y) ** 2)
        # Base opacity on distance, with a maximum transparency (lower alpha) as distance increases
        max_distance = 200  # Distance at which the alpha will be fully transparent
        alpha = max(0, int(255 * (1 - (distance / max_distance))))  # Decreasing opacity with distance
        trail_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        trail_surface.fill((*color, alpha))
        surface.blit(trail_surface, (x, y))

def update_square_position():
    global square_x, square_y, square_size, current_color, current_color_name, available_colors
    
    square_x += velocity[0]
    square_y += velocity[1]

    # Bounce off the edges and change size and color
    if square_x <= 0 or square_x + square_size >= width or square_y <= 0 or square_y + square_size >= height:
        if square_x <= 0 or square_x + square_size >= width:
            velocity[0] = -velocity[0]
        if square_y <= 0 or square_y + square_size >= height:
            velocity[1] = -velocity[1]
        
        # Change square size
        square_size += 10

        # Update color
        if not available_colors:
            available_colors = all_colors.copy()
            available_colors.remove(current_color)
        current_color = available_colors.pop()
        current_color_name = color_names[current_color]

    # Ensure the square doesn't go out of bounds
    if square_x < 0:
        square_x = 0
    if square_x + square_size > width:
        square_x = width - square_size
    if square_y < 0:
        square_y = 0
    if square_y + square_size > height:
        square_y = height - square_size

def draw_square():
    pygame.draw.rect(screen, current_color, (square_x, square_y, square_size, square_size))

def display_color_name():
    font = pygame.font.Font(None, 36)
    text = font.render(current_color_name, True, (255, 255, 255))
    screen.blit(text, (10, 10))

def update_trail():
    # Add the current square position to the trail
    trail.append((square_x, square_y, square_size, current_color))
    
    # Limit trail length to include extra trailing squares
    if len(trail) > 6:  # Allowing for three extra squares
        trail.pop(0)

def main():
    global running
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_square_position()

        # Stop the simulation if the square fills the screen
        if square_size >= width or square_size >= height:
            running = False

        # Clear the screen
        screen.fill(black)
        
        # Draw the trail
        draw_trail(screen, trail)
        
        # Draw the square
        draw_square()
        
        # Draw the color name
        display_color_name()

        # Update the trail
        update_trail()
        
        # Update the display
        pygame.display.flip()

        # Delay to control frame rate
        pygame.time.delay(30)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
