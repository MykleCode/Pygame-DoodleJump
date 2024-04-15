from math import copysign
import pygame
from singleton import Singleton
from sprite import Sprite
from level import Level
import settings as config

pygame.mixer.init()

# Returning values: (x < 0 => -1) & (x > 0 => 1) & (x == 0 => 0)
getsign = lambda x: copysign(1, x)

class Player(Sprite, Singleton):
    # Initialization using a shared dictionary
    def __init__(self, *args):
        Sprite.__init__(self, *args)
        self.__startrect = self.rect.copy()  # Create the main rect
        self.__maxvelocity = pygame.Vector2(config.PLAYER_MAX_SPEED, 100)  # Create a vector with x, y coordinates
        self.__startspeed = 1.5  # Initial speed, increases over time
        self._velocity = pygame.Vector2()  # Create a vector
        self._input = 0  # Input check
        self._jumpforce = config.PLAYER_JUMPFORCE  # Jump force
        self._bonus_jumpforce = config.PLAYER_BONUS_JUMPFORCE  # Bonus jump force
        self.gravity = config.GRAVITY  # Gravity
        self.accel = 0.5  # Acceleration
        self.deccel = 0.6  # Deceleration
        self.dead = False  # Whether dead or not
        self.model = pygame.image.load(config.jumping[0]).convert_alpha()  # Model
        self.tag = 'player'  # Tag
        self.direction = ''  # Direction
        self.condition = ''  # Current condition

    def _fix_velocity(self):
        # Set velocity between minimum and maximum values
        self._velocity.y = min(self._velocity.y, self.__maxvelocity.y)
        self._velocity.y = round(max(self._velocity.y, -self.__maxvelocity.y), 2)
        self._velocity.x = min(self._velocity.x, self.__maxvelocity.x)
        self._velocity.x = round(max(self._velocity.x, -self.__maxvelocity.x), 2)

    def reset(self):
        # Reset the game
        self._velocity = pygame.Vector2()
        self.rect = self.__startrect.copy()
        self.camera_rect = self.__startrect.copy()
        self.dead = False

    def handle_event(self, event: pygame.event.Event):
        # Check for movement initiation
        if event.type == pygame.KEYDOWN:
            # Left-right movement
            if event.key == pygame.K_a:  # Left
                self._velocity.x = -self.__startspeed
                self._input = -1
                self.left = True
                self.right = False
                self.direction = 'left'
            elif event.key == pygame.K_d:  # Right
                self._velocity.x = self.__startspeed
                self._input = 1
                self.right = True
                self.left = False
                self.direction = 'right'

        # Check for movement cessation
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_a and self._input == -1) or (event.key == pygame.K_d and self._input == 1):
                self._input = 0

    def jump(self, force: float = None):
        # Jump
        if not force:  # If force is None or False
            force = self._jumpforce  # Assign jump force
        self._velocity.y = -force  # Change the y-component of the velocity vector

    def onCollide(self, obj: Sprite):
        # Collision with the upper part of a platform
        self.rect.bottom = obj.rect.top
        self.jump()

    def get_status(self):
        # Get movement status
        if 0.5 > self._velocity.y >= -21:
            self.condition = 'jumping'
        elif self._velocity.y < -21:
            self.condition = 'bonus_effect'
        else:
            self.condition = 'falling'

    def collisions(self):
        # Collisions
        lvl = Level.instance  # Instance of the Level class
        if not lvl:  # If the instance doesn't exist, return None and stop execution
            return
        for platform in lvl.platforms:  # Iterate through platforms
            # Check for falling or collision
            if self._velocity.y > 0.5:  # Vertical speed is greater, indicating the object should fall
                # Check for collision with a bonus
                if platform.bonus and pygame.sprite.collide_rect(self, platform.bonus):
                    config.explosion.play()  # Play explosion sound
                    self.onCollide(platform.bonus)
                    platform.bonus.effect = True
                    self.jump(platform.bonus.force)  # Apply higher jump force
                    self.bonus_effect_start_time = pygame.time.get_ticks()
                # Check for collision with a platform
                if pygame.sprite.collide_rect(self, platform):
                    config.jump.play()  # Play jump sound
                    self.onCollide(platform)
                    platform.onCollide()

    def update(self):
        # Player movement
        if self.camera_rect.y > config.YWIN * 2:
            self.dead = True
            return
        # Update velocity (applying gravity, input data)
        self._velocity.y += self.gravity  # Change velocity based on gravity
        if self._input:  # Accelerate along the x-axis when a key is pressed
            self._velocity.x += self._input * self.accel
        elif self._velocity.x:  # Decelerate along the x-axis when no key is pressed
            self._velocity.x -= getsign(self._velocity.x) * self.deccel
            self._velocity.x = round(self._velocity.x)
        self._fix_velocity()

        # Update position
        self.rect.x = (self.rect.x + self._velocity.x) % (config.XWIN - self.rect.width)  # Update horizontal position
        self.rect.y += self._velocity.y  # Update vertical position

        self.collisions()
