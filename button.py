import pygame

# Class for management buttons in interface
class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, action=None): 
        super().__init__()
        self.image = image 
        self.rect = self.image.get_rect(center=pos)
        self.action = action # Triggered function
    
    # Run function on mouse click
    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos): # If there is collision
            self.action() # Launching