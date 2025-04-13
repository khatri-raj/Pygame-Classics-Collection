# Flappy Bird Clone
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants    
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)
        self.velocity = 0

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Keep bird on screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        if is_top:
            height = y
            y = 0
        else:
            height = WINDOW_HEIGHT - y
            
        self.image = pygame.Surface((50, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        
        # Create bird
        self.bird = Bird()
        self.all_sprites.add(self.bird)
        
        # Font for score
        self.font = pygame.font.Font(None, 36)

    def spawn_pipes(self):
        now = pygame.time.get_ticks()
        if now - self.last_pipe > PIPE_FREQUENCY:
            self.last_pipe = now
            gap_y = random.randint(100, WINDOW_HEIGHT - 100 - PIPE_GAP)
            
            # Top pipe
            pipe_top = Pipe(WINDOW_WIDTH, gap_y, True)
            # Bottom pipe
            pipe_bottom = Pipe(WINDOW_WIDTH, gap_y + PIPE_GAP, False)
            
            self.pipes.add(pipe_top)
            self.pipes.add(pipe_bottom)
            self.all_sprites.add(pipe_top)
            self.all_sprites.add(pipe_bottom)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()

    def update(self):
        self.all_sprites.update()
        self.spawn_pipes()
        
        # Check for collisions
        if pygame.sprite.spritecollide(self.bird, self.pipes, False):
            self.running = False
            
        # Update score
        for pipe in self.pipes:
            if pipe.rect.right < self.bird.rect.left and not hasattr(pipe, 'scored'):
                pipe.scored = True
                self.score += 0.5  # Count each pair of pipes as 1 point

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {int(self.score)}', True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
        
        print(f"Final Score: {int(self.score)}")
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
 