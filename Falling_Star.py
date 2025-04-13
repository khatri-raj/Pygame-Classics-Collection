# Falling Star
import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 8
        self.color = BLUE
        self.bullets = []

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            bullet.draw(window)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self):
        bullet = Bullet(self.x + self.width // 2, self.y)
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 5
        self.color = RED

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y -= self.speed

class Asteroid:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(3, 7)
        self.color = WHITE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed

def check_collision(bullet, asteroid):
    bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, 
                            bullet.radius * 2, bullet.radius * 2)
    asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
    return bullet_rect.colliderect(asteroid_rect)

# Game settings
player = Player()
asteroids = []
asteroid_spawn_rate = 30
score = 0
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Spawn asteroids
    if random.randint(1, asteroid_spawn_rate) == 1:
        asteroids.append(Asteroid())

    # Update game objects
    player.move()
    player.update_bullets()

    # Update asteroids and check collisions
    for asteroid in asteroids[:]:
        asteroid.move()
        
        # Remove asteroid if it goes off screen
        if asteroid.y > HEIGHT:
            asteroids.remove(asteroid)
            
        # Check bullet collisions
        for bullet in player.bullets[:]:
            if check_collision(bullet, asteroid):
                if asteroid in asteroids:
                    asteroids.remove(asteroid)
                if bullet in player.bullets:
                    player.bullets.remove(bullet)
                score += 10

        # Check player collision
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
        if player_rect.colliderect(asteroid_rect):
            running = False

    # Draw everything
    window.fill(BLACK)
    player.draw(window)
    for asteroid in asteroids:
        asteroid.draw(window)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

# Game over screen
window.fill(BLACK)
game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
window.blit(game_over_text, text_rect)
pygame.display.update()

# Wait a few seconds before closing
pygame.time.wait(3000)

pygame.quit()
