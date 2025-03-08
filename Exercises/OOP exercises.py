# OOP concepts review
'''
definitions: (and its role in OOP)
class: a blueprint for creating objects
object: an instance of a class
attribute: a variable that is part of a class   
method: a function that is part of a class
inheritance: a way to form new classes using classes that have already been defined
encapsulation: the concept of restricting access to some of an object's components
polymorphism: a way to use a method in different ways for different data input
'''
# Q2: Creating a simple game character class
import pygame
import math

class Player:
    def __init__(self, x, y, sprite_path):
        """Initialize player with position, health, and sprite."""
        self.x = x
        self.y = y
        self.health = 100  # Default health
        self.sprite = pygame.image.load(sprite_path)  # Load sprite from file

    def move(self, dx, dy):
        """Move player by dx, dy."""
        self.x += dx
        self.y += dy

    def take_damage(self, amount):
        """Reduce player health by the given amount, ensuring it doesn't go below zero."""
        self.health = max(0, self.health - amount)

    def draw(self, screen):
        """Draw the player sprite at its current position."""
        screen.blit(self.sprite, (self.x, self.y))

# Q3: Extending the game with enemy class

class Enemy:
    def __init__(self, x, y, speed, sprite):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite = pygame.image.load(sprite)  # Load the sprite image
        self.rect = self.sprite.get_rect(center=(x, y))  # Get the rect for positioning

    def move_towards(self, target_x, target_y):
        # Calculate direction vector
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx /= distance  # Normalize
            dy /= distance

            # Move enemy towards target
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.rect.center = (self.x, self.y)  # Update rect position

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)  # Draw the enemy on the screen

# Q4: integrating classes into pygame loop

# Create instances
player = Player(100, 100, 4)
enemy = Enemy(300, 100, 2)
player_health = 100

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Enemy movement towards player
    enemy.move_towards(player.x, player.y)

    # Check collision (simple AABB collision detection)
    if player.rect.colliderect(enemy.rect):
        player_health -= 1  # Reduce health if enemy touches player
        print(f"Player Health: {player_health}")

    # Draw everything
    player.draw(screen)
    enemy.draw(screen)

    # Update screen
    pygame.display.flip()

pygame.quit()
