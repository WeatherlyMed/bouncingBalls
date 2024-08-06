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
speed = 5
angle = random.uniform(0, 2 * math.pi)
velocity = [speed * math.cos(angle), speed * math.sin(angle)]

# List of concentric squares (outermost to innermost)
num_squares = 12  # Double the number of outer squares
concentric_squares = []
square_gap = width // (num_squares * 2)

for i in range(num_squares):
    size = width - 2 * i * square_gap
    x = i * square_gap
    y = i * square_gap
    color = colors[i % len(colors)]
    concentric_squares.append({'x': x, 'y': y, 'size': size, 'color': color})

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

def draw_square_outline(square):
    pygame.draw.rect(screen, square['color'], (square['x'], square['y'], square['size'], square['size']), 1)

def update_bouncing_square():
    bouncing_square['x'] += bouncing_square['velocity'][0]
    bouncing_square['y'] += bouncing_square['velocity'][1]

    # Check for collisions with the concentric squares
    for outer_square in concentric_squares[:]:
        if (
            bouncing_square['x'] <= outer_square['x'] or
            bouncing_square['x'] + bouncing_square['size'] >= outer_square['x'] + outer_square['size']
        ):
            bouncing_square['velocity'][0] = -bouncing_square['velocity'][0]
            if outer_square in concentric_squares:
                create_particles(bouncing_square['x'] + bouncing_square['size'] // 2, 
                                 bouncing_square['y'] + bouncing_square['size'] // 2, outer_square['color'])
                concentric_squares.remove(outer_square)

        if (
            bouncing_square['y'] <= outer_square['y'] or
            bouncing_square['y'] + bouncing_square['size'] >= outer_square['y'] + outer_square['size']
        ):
            bouncing_square['velocity'][1] = -bouncing_square['velocity'][1]
            if outer_square in concentric_squares:
                create_particles(bouncing_square['x'] + bouncing_square['size'] // 2, 
                                 bouncing_square['y'] + bouncing_square['size'] // 2, outer_square['color'])
                concentric_squares.remove(outer_square)

    # Ensure the square doesn't go out of bounds
    if bouncing_square['x'] < 0:
        bouncing_square['x'] = 0
    if bouncing_square['x'] + bouncing_square['size'] > width:
        bouncing_square['x'] = width - bouncing_square['size']
    if bouncing_square['y'] < 0:
        bouncing_square['y'] = 0
    if bouncing_square['y'] + bouncing_square['size'] > height:
        bouncing_square['y'] = height - bouncing_square['size']

def main():
    global running
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_bouncing_square()
        update_particles()

        # Clear the screen
        screen.fill(black)

        # Draw the concentric squares
        for square in concentric_squares:
            draw_square_outline(square)

        # Draw the bouncing square
        pygame.draw.rect(screen, bouncing_square['color'], 
                         (bouncing_square['x'], bouncing_square['y'], 
                          bouncing_square['size'], bouncing_square['size']))

        # Draw particles
        draw_particles()

        # Update the display
        pygame.display.flip()

        # Check if all outer squares are broken
        if not concentric_squares:
            running = False

        # Delay to control frame rate
        pygame.time.delay(30)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
