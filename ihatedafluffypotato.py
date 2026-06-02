import pygame

# Initialize Pygame constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """Initializes the player's texture, positioning, and speed metrics."""
        super().__init__()
        
        # Create a simple placeholder square for the player texture
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255)) # Blue color
        
        # Pygame Rect handles positioning and collisions 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Custom movement attributes
        self.speed = 5

    def handle_input(self):
        """Monitors real-time keystrokes to calculate player intentions."""
        keys = pygame.key.get_pressed()
        
        self.velocity_x = 0
        self.velocity_y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed

    def update(self):
        """Updates the player state and ensures they stay within screen bounds."""
        # Process keystroke updates first
        self.handle_input()
        
        # Displace player location vector
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Screen border containment checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, surface):
        """Draws the player's texture onto the main active game window."""
        surface.blit(self.image, self.rect)
