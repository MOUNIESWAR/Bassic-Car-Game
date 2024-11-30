import pygame
import random
import time
import os
import json

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Load images
def load_image(name, scale=1):
    try:
        image = pygame.image.load(os.path.join("assets", name))
        if scale != 1:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except:
        return None

# Create assets directory if it doesn't exist
if not os.path.exists("assets"):
    os.makedirs("assets")

# Load or create high score
def load_high_score():
    try:
        with open("high_score.json", "r") as f:
            return json.load(f)["high_score"]
    except:
        return 0

def save_high_score(score):
    with open("high_score.json", "w") as f:
        json.dump({"high_score": score}, f)

# Power-up class
class PowerUp:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height
        self.speed = 3
        self.type = random.choice(["shield", "speed", "points"])
        self.color = BLUE if self.type == "shield" else YELLOW if self.type == "speed" else GREEN

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed
        return self.y > WINDOW_HEIGHT

# Player car
class PlayerCar:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - self.height - 20
        self.base_speed = 5
        self.speed = self.base_speed
        self.color = RED
        self.shield = False
        self.shield_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        if self.shield:
            pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height), 3)

    def move(self):
        keys = pygame.key.get_pressed()
        current_speed = self.speed * 1.5 if self.speed_boost else self.speed
        
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= current_speed
        if keys[pygame.K_RIGHT] and self.x < WINDOW_WIDTH - self.width:
            self.x += current_speed

    def update(self, current_time):
        if self.shield and current_time > self.shield_time:
            self.shield = False
        if self.speed_boost and current_time > self.speed_boost_time:
            self.speed_boost = False

# Enemy car
class EnemyCar:
    def __init__(self, base_speed):
        self.width = 50
        self.height = 80
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height
        self.base_speed = base_speed
        self.speed = base_speed + random.uniform(-1, 1)
        self.color = GREEN

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed
        return self.y > WINDOW_HEIGHT

# Road marking class for animation
class RoadMark:
    def __init__(self, y):
        self.width = 10
        self.height = 40
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = y
        self.speed = 5

    def move(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = -self.height

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))

def check_collision(player, enemy):
    if player.shield:
        return False
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
    return player_rect.colliderect(enemy_rect)

def check_powerup_collision(player, powerup):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    powerup_rect = pygame.Rect(powerup.x, powerup.y, powerup.width, powerup.height)
    return player_rect.colliderect(powerup_rect)

def main():
    clock = pygame.time.Clock()
    player = PlayerCar()
    enemies = []
    powerups = []
    road_marks = [RoadMark(y) for y in range(0, WINDOW_HEIGHT, 100)]
    score = 0
    high_score = load_high_score()
    game_over = False
    font = pygame.font.Font(None, 36)
    start_time = time.time()
    base_enemy_speed = 4

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    player = PlayerCar()
                    enemies = []
                    powerups = []
                    score = 0
                    game_over = False
                    start_time = time.time()
                    base_enemy_speed = 4

        if not game_over:
            # Increase difficulty over time
            base_enemy_speed = 4 + (elapsed_time // 30)
            spawn_chance = 0.02 + (elapsed_time // 60) * 0.01
            spawn_chance = min(spawn_chance, 0.1)

            # Spawn new enemy
            if random.random() < spawn_chance:
                enemies.append(EnemyCar(base_enemy_speed))

            # Spawn power-up
            if random.random() < 0.005:  # 0.5% chance each frame
                powerups.append(PowerUp())

            # Move player
            player.move()
            player.update(current_time)

            # Move road marks
            for mark in road_marks:
                mark.move()

            # Move enemies and check for collisions
            for enemy in enemies[:]:
                if enemy.move():
                    enemies.remove(enemy)
                    score += 1
                elif check_collision(player, enemy):
                    game_over = True
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)

            # Move and check power-ups
            for powerup in powerups[:]:
                if powerup.move():
                    powerups.remove(powerup)
                elif check_powerup_collision(player, powerup):
                    if powerup.type == "shield":
                        player.shield = True
                        player.shield_time = current_time + 5  # 5 seconds shield
                    elif powerup.type == "speed":
                        player.speed_boost = True
                        player.speed_boost_time = current_time + 3  # 3 seconds speed boost
                    elif powerup.type == "points":
                        score += 10
                    powerups.remove(powerup)

            # Draw everything
            window.fill(BLACK)
            
            # Draw road marks
            for mark in road_marks:
                mark.draw(window)

            player.draw(window)
            for enemy in enemies:
                enemy.draw(window)
            for powerup in powerups:
                powerup.draw(window)

            # Draw score and high score
            score_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            window.blit(score_text, (10, 10))
            window.blit(high_score_text, (10, 50))
        else:
            # Game over screen
            game_over_text = font.render("Game Over! Press SPACE to restart", True, WHITE)
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            window.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//2))
            window.blit(final_score_text, (WINDOW_WIDTH//2 - final_score_text.get_width()//2, WINDOW_HEIGHT//2 + 50))
            window.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, WINDOW_HEIGHT//2 + 100))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
