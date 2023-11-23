import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift Game")

# Load the map image
map_image = pygame.image.load("carro.png")  # Replace with your map image file

# Load the car image
car_image = pygame.image.load("map.png")  # Replace with your car image file
car_rect = car_image.get_rect()
car_rect.center = (WIDTH // 2, HEIGHT // 2)  # Starting position of the car

# Variables
speed = 5
angle = 0

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle += 5
        
    if keys[pygame.K_RIGHT]:  
        angle -= 5

    # Move the car
    angle_rad = angle * (3.1416 / 180)  # Convert angle to radians for trig functions
    car_rect.x += speed * math.cos(angle_rad)
    car_rect.y -= speed * math.sin(angle_rad)

    # Draw everything
    screen.fill(WHITE)
    screen.blit(map_image, (0, 0))  # Draw the map
    rotated_car = pygame.transform.rotate(car_image, angle)  # Rotate the car image
    screen.blit(rotated_car, car_rect.topleft)  # Draw the car
    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
