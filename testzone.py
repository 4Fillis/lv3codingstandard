import pygame

# 1. Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

# Object properties
x, y = 250, 250
speed = 5

running = True
while running:
    # 2. Event Handling (Check for window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. Continuous Key Detection
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  x -= speed
    if keys[pygame.K_RIGHT]: x += speed
    if keys[pygame.K_UP]:    y -= speed
    if keys[pygame.K_DOWN]:  y += speed

    # 4. Redraw Everything
    screen.fill((0, 0, 0)) # Clear screen with black
    pygame.draw.rect(screen, (100, 100, 100), (x, y, 20, 40)) # Draw red square
    pygame.display.update()

    # Control frame rate
    clock.tick(60)

pygame.quit()