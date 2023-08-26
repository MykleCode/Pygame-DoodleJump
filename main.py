from MARWIN_ADVENTURE import *
from button import Button
import pygame, sys
from singleton import Singleton
from camera import Camera
from player import Player
from level import Level
import settings as config
pygame.init()

# Window
window = pygame.display.set_mode(config.DISPLAY,config.FLAGS)
clock = pygame.time.Clock()

# Function for displaying text
def display_text(text, font_size, color, font_path, pos):
    font = pygame.font.Font(font_path, font_size)
    text_render = font.render(text, True, color) 
    text_rect = text_render.get_rect(center=pos)
    window.blit(text_render, text_rect) 

class Game(Singleton):
	# Class for managing the game
	def __init__(self):
		# Initialization
		self.score = 0 # Record
		self.paused = False # Pause
		self.max_darkness_reached = False # Has maximum darkness been reached
		self.frame_reverse_animation_end = True # End of reverse frame animation
		self.frame_animation_end = False # End of frame animation
		self.game_over_animation_end = False # End of game over image animation
		# End of button animation
		self.mainmenu_button_animation_end = False 
		self.restart_button_animation_end = False

		# Game over
		self.game_over_image = pygame.image.load(config.game_over_image).convert()
		self.gameover_rect_initial_y = -config.HALF_YWIN  # Initial position of game over vertically
		self.gameover_rect_y = self.gameover_rect_initial_y  # Current offset of game over vertically
		self.gameover_rect = self.game_over_image.get_rect(center=(config.HALF_XWIN,config.HALF_YWIN//3)) # Get image size
		self.game_over_sound_played = False

		# Frame images for pause, score
		self.frame_image_pause = pygame.image.load(config.frame_image_pause).convert()
		self.frame_image_score = pygame.image.load(config.frame_image_score).convert()
		self.frame_rect_initial_y = -20  # Initial position of frame vertically
		self.frame_rect_y = self.frame_rect_initial_y  # Current offset of frame vertically
		
		# Buttons: mainmenu, restart, resume
		self.mainmenu_button_rect_initial_x = 0  # Initial position of mainmenu horizontally
		self.restart_button_rect_initial_x = config.XWIN  # Initial position of restart horizontally
		self.mainmenu_button_image = pygame.image.load(config.mainmenu_button_non_active)
		self.restart_button_image = pygame.image.load(config.restart_button_non_active)
		self.resume_button_image = pygame.image.load(config.resume_button_non_active)

		# Button sounds
		self.mainmenu_button_sound = False
		self.restart_button_sound = False
		self.resume_button_sound = False

		# Background
		self.background_image = pygame.image.load(config.background_image).convert()
		self.background_image = pygame.transform.scale(self.background_image, (config.XWIN, config.YWIN))
		self.overlay_color = config.BLACK  # Dimming color
		self.overlay_alpha = 200  # Dimming alpha channel

		######################Class instances######################
		# Buttons
		#For game over
		self.mainmenu_button = Button(self.mainmenu_button_image, (self.mainmenu_button_rect_initial_x, config.YWIN // 1.2), action='')
		self.restart_button = Button(self.restart_button_image, (self.restart_button_rect_initial_x, config.YWIN // 1.2), action='')
		# For pause
		self.mainmenu_button_pause = Button(self.mainmenu_button_image, (config.XWIN // 4, config.YWIN // 2), action='')
		self.restart_button_pause = Button(self.restart_button_image, (config.XWIN // 2, config.YWIN // 2), action='')
		self.resume_button = Button(self.resume_button_image, (config.XWIN // 1.34, config.YWIN // 2), action='')
		# Objects
		self.camera = Camera() # Camera
		self.lvl = Level() # Level
		self.player = Player( # Player
			config.HALF_XWIN - config.PLAYER_SIZE[0]/2, # X position
			config.HALF_YWIN + config.HALF_YWIN/2, # Y position
			*config.PLAYER_SIZE,) # Size
	
	def resume(self): # Resume pause
		self.paused = False
		
	def reset(self): # Reset the game
		if self.game_over_animation_end or self.paused:
			pygame.mixer.music.play(-1)
			self.paused = False
			self.camera.reset()
			self.lvl.reset()
			self.player.reset()

	def launch_main_menu(self): # Launch main menu and exit current loop
		import MARWIN_ADVENTURE
		MARWIN_ADVENTURE.Run()
		pygame.quit()
		sys.exit()

	def _event_loop(self): # Event handling
		# User events
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#self.close()
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_ESCAPE: # Pause
					self.paused = not self.paused # Toggle value
			elif event.type == pygame.MOUSEBUTTONDOWN: 
				if self.player.dead: # If game over, process menu buttons to prevent false clicks
					self.mainmenu_button.check_click(mouse_pos)
					self.restart_button.check_click(mouse_pos)
				if self.paused: # If paused, process pause menu buttons
					self.resume_button.check_click(mouse_pos)
					self.mainmenu_button_pause.check_click(mouse_pos)
					self.restart_button_pause.check_click(mouse_pos)

			if not self.paused: # If not paused, process user events
				self.player.handle_event(event)

	def _update_loop(self):
		# Update surfaces
		self.player.update()
		self.lvl.update()

		if not self.player.dead:
			self.camera.update(self.player.rect) # Update camera movement
			# Calculate score and display it
			self.score=-self.camera.state.y//50 # Update score

	def _render_loop(self):
		global window, clock
		# Display objects

		# Calculate background offset based on camera position
		offset_y = -self.camera.state.y % config.YWIN
		# Display background
		window.blit(self.background_image, (0, offset_y)) 
		window.blit(self.background_image, (0, offset_y - config.YWIN))

		# Draw objects using Sprite.py
		self.lvl.draw(window)
		self.player.draw(window)

		# Assign functions to buttons
		# Buttons for game over
		self.mainmenu_button.action = self.launch_main_menu
		self.restart_button.action = self.reset
		# Buttons for pause
		self.resume_button.action = self.resume
		self.mainmenu_button_pause.action = self.launch_main_menu
		self.restart_button_pause.action = self.reset
		
		################## DRAWING OBJECTS BASED ON EVENTS ##################
		if not self.player.dead and self.paused: # Pause
			mouse_pos = pygame.mouse.get_pos() # Get current mouse position
			window.blit(self.frame_image_pause, (pygame.math.Vector2(config.HALF_XWIN - 185, config.YWIN // 4 - 50))) # Draw frame for text
			display_text('PAUSE', 65, config.WHITE, config.pixel_font, (pygame.math.Vector2(config.HALF_XWIN, config.YWIN // 4))) # Draw "PAUSE" text
			
			# Handle button hover reactions
            # Resume button
			if self.resume_button.rect.collidepoint(mouse_pos):  # If collision, switch to active image
				if self.resume_button_sound: # Play button sound only once
					config.check_button.play()
					self.resume_button_sound = False
				window.blit(pygame.image.load(config.resume_button_active).convert(), self.resume_button.rect)
			else: # Change to default image
				self.resume_button_sound = True
				window.blit(self.resume_button.image.convert(), self.resume_button.rect) 

			# Main menu
			if self.mainmenu_button_pause.rect.collidepoint(mouse_pos): # If there is collision, change to active image
				if self.mainmenu_button_sound: # Play button sound only once
					config.check_button.play()
					self.mainmenu_button_sound = False
				window.blit(pygame.image.load(config.mainmenu_button_active).convert(), self.mainmenu_button_pause.rect)
			else: # Change to default image
				self.mainmenu_button_sound = True
				window.blit(self.mainmenu_button_pause.image.convert(), self.mainmenu_button_pause.rect)

			# Restart
			if self.restart_button_pause.rect.collidepoint(mouse_pos): # If there is collision, change to active image 
				if self.restart_button_sound: # Play button sound only once
					config.check_button.play()
					self.restart_button_sound = False
				window.blit(pygame.image.load(config.restart_button_active).convert(), self.restart_button_pause.rect)
			else: # Change to default image
				self.restart_button_sound = True
				window.blit(self.restart_button_pause.image.convert(), self.restart_button_pause.rect)

		if self.player.dead: # Game over
			# Zeroing the results of the frame if the animation is over
			if self.frame_animation_end: 
				self.frame_rect_y = self.frame_rect_initial_y
				self.frame_animation_end = False
			self.frame_reverse_animation_end = False 

			if config.music_volume >= 0.0:
				config.music_volume -= 0.001
			pygame.mixer.music.set_volume(config.music_volume)

			# Screen dimming
			self.overlay_alpha = min(self.overlay_alpha + 5, 200)
			if self.overlay_alpha >= 200:
				self.max_darkness_reached = True

				# Animation of moving buttons and images
				# Game over
				if self.gameover_rect_y < 15:
					self.gameover_rect_y += 10
				else:
					self.game_over_animation_end = True
				
				# Main menu button
				if self.mainmenu_button.rect.x < config.XWIN // 3 - self.mainmenu_button.rect[2] // 2:
					self.mainmenu_button.rect.x += 10
				else:
					self.mainmenu_button_animation_end = True
				
				# Restart button
				if self.restart_button.rect.x > config.XWIN // 1.5 - self.restart_button.rect[2] // 2:
					self.restart_button.rect.x -= 13
				else:
					self.restart_button_animation_end = True

		else:
			# Zeroing values
            # Decrease the alpha channel of the fade over time (this is where the fade rate is set)
			if config.music_volume < 0.1:
				config.music_volume += 0.01
			pygame.mixer.music.set_volume(config.music_volume)
			self.game_over_sound_played = False
			self.overlay_alpha = max(self.overlay_alpha - 5, 0)
			self.max_darkness_reached = False
			self.game_over_animation_end = False
			self.mainmenu_button_animation_end = False
			self.restart_button_animation_end = False
			self.score_txt_visible = True
			self.gameover_rect_y = self.gameover_rect_initial_y
			self.mainmenu_button.rect.x = self.mainmenu_button_rect_initial_x
			self.restart_button.rect.x = self.restart_button_rect_initial_x
		
		# Creating a surface and applying shading to it
		overlay_surface = pygame.Surface((config.XWIN, config.YWIN))
		overlay_surface.fill(self.overlay_color)
		overlay_surface.set_alpha(self.overlay_alpha)
		if self.overlay_alpha != 0:
			self.score_txt_visible = False
			window.blit(overlay_surface, (0, 0))
		
		# Game process
		if self.score_txt_visible or not self.frame_reverse_animation_end:
			# High score counter animation
			if not self.frame_animation_end and self.score_txt_visible:
				if self.frame_rect_y < 10:
					self.frame_rect_y += 2
				else:
					self.frame_animation_end = True
			
			# High score counter animation
			elif not self.frame_reverse_animation_end:
				if self.frame_rect_y >= -50:
					self.frame_rect_y -= 10
				else:
					self.frame_reverse_animation_end = True

			# Displaying
			window.blit(self.frame_image_score, (config.XWIN // 6, self.frame_rect_y)) # Frame
			display_text(str(self.score) + "m", 30, config.WHITE, config.pixel_font, (pygame.math.Vector2(config.XWIN // 3.1, self.frame_rect_y + 25))) # Score text

		# Displaying game over objects
		if self.max_darkness_reached: # if darkening ended
			if not self.game_over_sound_played:
				config.game_over.play()
				self.game_over_sound_played = True

			window.blit(self.game_over_image, (config.HALF_XWIN - self.gameover_rect.width // 2, self.gameover_rect_y)) # Displaying game over images
			display_text(" SCORE:" + str(self.score) + "m", 40, config.WHITE, config.pixel_font, (config.HALF_XWIN, self.gameover_rect_y + config.YWIN // 1.5)) # Displaying score
			mouse_pos = pygame.mouse.get_pos() # Getting mouse position
				
			# Processing the reaction of buttons on hovering the cursor
			# Main menu
			if self.mainmenu_button.rect.collidepoint(mouse_pos) and self.game_over_animation_end: # If there is collision, change to active image 
				if self.mainmenu_button_sound: # Play button sound only once
					config.check_button.play()
					self.mainmenu_button_sound = False
				window.blit(pygame.image.load(config.mainmenu_button_active).convert(), self.mainmenu_button.rect)
			else: # Change to default image
				self.mainmenu_button_sound = True
				window.blit(self.mainmenu_button.image.convert(), self.mainmenu_button.rect)

			# Restart
			if self.restart_button.rect.collidepoint(mouse_pos) and self.game_over_animation_end: # If there is collision, change to active image 
				if self.restart_button_sound: # Play button sound only once
					config.check_button.play()
					self.restart_button_sound = False
				window.blit(pygame.image.load(config.restart_button_active).convert(), self.restart_button.rect)
			else: # Change to default image
				self.restart_button_sound = True
				window.blit(self.restart_button.image.convert(), self.restart_button.rect)
        
		# Updating scene
		pygame.display.update()
		clock.tick(config.FPS)

	def run(self):
		# Main game loop
		pygame.mixer.music.load(config.level_music)
		pygame.mixer.music.set_volume(config.music_volume)
		pygame.mixer.music.play(-1)
		while True:
			self._event_loop() # Event handling
			self._render_loop() # Event render
			if not self.paused:
				self._update_loop() # Update surface

def run_game(): # Game launch function
	game = Game()
	game.run()

if __name__ == "__main__":
	# Program start
	run_game()




