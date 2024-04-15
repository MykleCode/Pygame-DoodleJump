import pygame
from singleton import Singleton
import settings as config

class Camera(Singleton):
    def __init__(self, lerp=8, width=config.XWIN, height=config.YWIN):
        # Initialize camera parameters: lerp (camera follow delay based on player's coordinates), width, height
        self.state = pygame.Rect(0, 0, width, height)  # Camera state
        self.lerp = lerp
        self.center = height // 2  # Camera center
        self.maxheight = self.center  # Maximum height
        
    def reset(self):
        # Reset function
        self.state.y = 0
        self.maxheight = self.center
    
    # Transform a rect relative to the camera's position
    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        # Take a rect as input and return a new rect moved by the negative y-coordinate of the top-left point
        return rect.move((0, -self.state.topleft[1]))
    
    # Return a new target rendering position based on the current camera position
    def apply(self, target: pygame.sprite.Sprite) -> pygame.Rect:
        # Take a rect as input and a Sprite (a sprite that wants to get a rendering position)
        # Return the required rect obtained from the apply_rect function, representing the rendering position for the target sprite
        return self.apply_rect(target.rect)
    
    # Method to move up to the maximum height achieved by the player
    def update(self, target: pygame.Rect):
        # Update the maximum height
        if target.y < self.maxheight:  # If the player reaches a new height on the screen
            self.lastheight = self.maxheight
            self.maxheight = target.y
        # Calculate the required camera follow speed
        speed = ((self.state.y + self.center) - self.maxheight) / self.lerp
        self.state.y -= speed
