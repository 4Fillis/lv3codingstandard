import pygame
import sys

# 1. Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Ground Example")
clock = pygame.time.Clock()

# 2. Game Variables & Physics
GRAVITY = 0.8
JUMP_STRENGTH = -16

# 3. Create Rectangles (Hitboxes)
# Player: [x, y, width, height]
player_rect = pygame.Rect(100, 100, 40, 60)
player_vel_y = 0
is_on_ground = False

# Ground and Platforms list
platforms = [
    pygame.Rect(0, 520, 800, 80),      # Main solid ground
    pygame.Rect(200, 400, 200, 20),    # Floating platform 1
    pygame.Rect(450, 300, 200, 20)     # Floating platform 2
]

# 4. Main Game Loop
running = True
while running:
    screen.fill((135, 206, 235))  # Clear screen with Sky Blue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Horizontal Input & Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5

    # Jumping Input (Only if touching the ground)
    if keys[pygame.K_SPACE] and is_on_ground:
        player_vel_y = JUMP_STRENGTH
        is_on_ground = False

    # Apply Gravity
    player_vel_y += GRAVITY
    
    # Move vertically FIRST, then check vertical ground collisions
    player_rect.y += player_vel_y
    is_on_ground = False  # Reset frame check

    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_vel_y > 0:  # Falling down onto the ground
                player_rect.bottom = platform.top
                player_vel_y = 0
                is_on_ground = True
            elif player_vel_y < 0:  # Hitting a platform from below
                player_rect.top = platform.bottom
                player_vel_y = 0

    # 5. Drawing elements
    # Draw Ground/Platforms (Dark Green)
    for platform in platforms:
        pygame.draw.rect(screen, (34, 139, 34), platform)

    # Draw Player (Red)
    pygame.draw.rect(screen, (255, 0, 0), player_rect)

    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()