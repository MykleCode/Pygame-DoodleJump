from button import Button
import pygame
import sys
import settings as config
pygame.init()

# Screen state flags
is_darkening = False  # Start darkening animation
is_finished_darkening = False  # Darkening animation finished
overlay_alpha = 0  # Darkness value

overlay_surface = pygame.Surface((config.XWIN, config.YWIN))  # Create surface for dimming
window = pygame.display.set_mode(config.DISPLAY, config.FLAGS)  # Screen
pygame.display.set_caption("MARWIN ADVENTURE")  # Set title
pygame.display.set_icon(pygame.image.load(config.icon))  # Set icon

BG = pygame.image.load(config.main_menu_background)  # Background

# Button images
play_button_image = pygame.image.load(config.start_button_non_active)  # START
exit_button_image = pygame.image.load(config.exit_button_non_active)  # EXIT

# Sound flags
play_button_PLAY_sound = False  # Play button sound activation
play_button_EXIT_sound = False  # Exit button sound activation

# Darkening animation
def darken_screen():
    global overlay_alpha, is_darkening, is_finished_darkening  # Global variables
    overlay_alpha += 5  # Increase darkness value
    if overlay_alpha >= 255:
        # Animation completion
        is_darkening = False
        is_finished_darkening = True
    overlay_surface.set_alpha(overlay_alpha)  # Set darkness
    if config.music_volume > 0.0:
        config.music_volume -= 0.001
    pygame.mixer.music.set_volume(config.music_volume)  # Apply reduced volume
    window.blit(overlay_surface, (0, 0))  # Draw

# Button action functions
def start_game():  # Start game for START button
    global is_darkening
    is_darkening = True
    play_button.clicked = True
    darken_screen()

def exit_game():  # Exit game for EXIT button
    pygame.quit()
    sys.exit()

# Text display
def display_text(text, font_size, color, font_path, pos):
    font = pygame.font.Font(font_path, font_size)
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect(center=pos)
    window.blit(text_render, text_rect)

# Button instances
play_button = Button(play_button_image, (config.XWIN // 2, config.YWIN // 2), action=start_game)
exit_button = Button(exit_button_image, (config.XWIN // 2, config.YWIN // 1.35), action=exit_game)

def Run():
    global overlay_alpha, is_darkening, is_finished_darkening, play_button_PLAY_sound, play_button_EXIT_sound
    # Reset before loop start
    config.music_volume = 0.2
    is_finished_darkening = False
    is_darkening = False
    overlay_alpha = 0

    # Load animation background
    bg_y = 0  # Background coordinates
    bg_speed = 1  # Background scroll speed

    # Start music
    pygame.mixer.music.load(config.overworld_music)
    pygame.mixer.music.set_volume(config.music_volume)
    pygame.mixer.music.play(-1)

    while True:
        mouse_pos = pygame.mouse.get_pos()  # Handle mouse position
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Button function activation on click
                play_button.check_click(mouse_pos)
                exit_button.check_click(mouse_pos)

        # If darkening animation finished, launch main.py
        if is_finished_darkening:
            pygame.mixer.music.stop()
            import main  # Import
            main.run_game()  # Initialization
            # Reset parameters after launch
            is_finished_darkening = False
            is_darkening = False
            overlay_alpha = 0

        # Display background and buttons
        window.blit(BG, (0, bg_y))
        window.blit(BG, (0, bg_y - config.YWIN))  # Extra display for covering image boundary

        # Update background position for vertical scrolling
        bg_y += bg_speed
        if bg_y >= config.YWIN:
            bg_y = 0

        # Display buttons and handle their hover reactions
        if not is_darkening or not is_finished_darkening:  # If not in darkening animation
            # Play button
            if play_button.rect.collidepoint(mouse_pos):
                if play_button_PLAY_sound:
                    config.check_button.play()
                    play_button_PLAY_sound = False
                window.blit(pygame.image.load(config.start_button_active), play_button.rect)
            else:
                play_button_PLAY_sound = True
                window.blit(play_button.image, play_button.rect)

            # Exit button
            if exit_button.rect.collidepoint(mouse_pos):
                if play_button_EXIT_sound:
                    config.check_button.play()
                    play_button_EXIT_sound = False
                window.blit(pygame.image.load(config.exit_button_active), exit_button.rect)
            else:
                play_button_EXIT_sound = True
                window.blit(exit_button.image, exit_button.rect)

            # Display MARWIN image
            display_text("MARWIN", 80, config.DARK_BLUE, config.pixel_font, (config.XWIN // 2, config.YWIN // 6))
            display_text("ADVENTURE", 80, config.DARK_BLUE, config.pixel_font, (config.XWIN // 2, config.YWIN // 3.5))

        if is_darkening:  # Screen darkening at game start
            darken_screen()

        pygame.display.update()  # Update screen
        pygame.time.Clock().tick(config.FPS)  # Set FPS

def main(): # Function to initialize launch, allowing to return to the main menu while in the game
    Run()

if __name__ == "__main__":
    # Program start
    main()
