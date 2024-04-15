import settings as config
from camera import Camera
import pygame

class Sprite:
    # Constructor for the sprite model
    def __init__(self, x: int, y: int, w: int, h: int):
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x, y, w, h)  # Create a rectangle to define the sprite's position on the screen
        self.camera_rect = self.rect.copy()  # Track the sprite's position for the camera

    def draw(self, surface: pygame.Surface):
        # Draw function
        if Camera.instance:  # If a camera instance is created
            self.camera_rect = Camera.instance.apply(self)  # Apply the rect of the current instance

            if self.tag == 'player':  # If it's the player
                self.get_status()  # Get the status
                if self.condition == 'jumping':
                    self.model = pygame.transform.scale(pygame.image.load(config.jumping[0]).convert_alpha(), (config.PLAYER_SIZE[0], config.PLAYER_SIZE[1]))  # Jumping model
                elif self.condition == 'falling':
                    self.model = pygame.transform.scale(pygame.image.load(config.falling[2]).convert_alpha(), (config.PLAYER_SIZE[0], config.PLAYER_SIZE[1]))  # Falling model
                elif self.condition == 'bonus_effect':
                    self.model = pygame.transform.scale(pygame.image.load(config.falling[3]).convert_alpha(), (config.PLAYER_SIZE[0], config.PLAYER_SIZE[1]))  # Bonus effect model

                if self.direction == 'left':  # Flip the image when moving in different directions
                    self.model = pygame.transform.flip(self.model, True, False)

                surface.blit(self.model, self.camera_rect)  # Draw with the applied model

            if self.tag == 'bonus':  # If it's a bonus
                if not self.effect:  # If not activated
                    self.model = pygame.transform.scale(pygame.image.load(config.bonus_default_image).convert_alpha(), (self.width, self.height))  # Default image
                else:
                    if not self.animation_finished:  # If animation is not finished
                        if self.bonus_effect_start_time is None:  # Assign animation start time
                            self.bonus_effect_start_time = pygame.time.get_ticks()

                        current_time = pygame.time.get_ticks()  # Total time
                        elapsed_time = current_time - self.bonus_effect_start_time  # Calculate remaining animation time

                        if elapsed_time >= self.bonus_effect_duration:  # If remaining time is greater than animation effect duration in ms
                            self.animation_finished = True  # Finish animation

                        # Determine current animation frame based on elapsed time and frame duration
                        self.current_frame = int(elapsed_time / (self.bonus_effect_duration / len(config.bonus_explosion)))
                        if self.current_frame >= len(config.bonus_explosion):
                            self.current_frame = len(config.bonus_explosion) - 1

                        self.model = pygame.image.load(config.bonus_explosion[self.current_frame]).convert_alpha()  # Apply image to model
                surface.blit(self.model, self.camera_rect)  # Draw

            if self.tag == 'platform':  # If it's a platform
                surface.blit(pygame.transform.scale(self.model, (self.width, self.height)), self.camera_rect)  # Draw the specified model
        else:
            surface.blit(self.model, self.rect)  # If no camera instance is created yet, draw the instance itself first
