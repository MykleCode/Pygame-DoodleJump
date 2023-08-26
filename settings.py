import pygame
from button import Button
pygame.init()

# Video settings
XWIN, YWIN = 800, 800  # Resolution
HALF_XWIN, HALF_YWIN = XWIN / 2, YWIN / 2  # Screen center
DISPLAY = (XWIN, YWIN)  # Create screen instance
FLAGS = pygame.DOUBLEBUF  # Screen options: 0 - none, pygame.FULLSCREEN - fullscreen, pygame.DOUBLEBUF - double buffering, pygame.SCALED - scaling
FPS = 60

# Fonts
pixel_font = 'graphics\\font\\font.ttf'

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GREEN = (131, 252, 107)
ANDROID_GREEN = (164, 198, 57)
FOREST_GREEN = (87, 189, 68)
DARK_BLUE = (2, 3, 28)

# Player
PLAYER_SIZE = (90, 60)  # Size: width, height
PLAYER_MAX_SPEED = 20  # Maximum speed
PLAYER_JUMPFORCE = 20  # Maximum acceleration
PLAYER_BONUS_JUMPFORCE = 70  # Maximum bonus acceleration
GRAVITY = 0.92  # Gravity

# Platform
PLATFORM_SIZE = (110, 10)  # Platform size
PLATFORM_DISTANCE_GAP = (50, 130)  # Distance between platforms
MAX_PLATFORM_NUMBER = 12  # Maximum number of platforms for generation
BONUS_WIDTH = 35  # Bonus width
BONUS_HEIGHT = 35  # Bonus height
BONUS_SPAWN_CHANCE = 6  # Bonus spawn chance
BREAKABLE_PLATFORM_CHANCE = 6  # Breakable platform spawn chance

# Music
music_volume = 0.2
level_music = 'audio\\level_music.wav'
overworld_music = 'audio\\overworld_music.wav'

# Sounds
sound_volume = 1
activate_button = 'audio\\effects\\activate_button.ogg'
check_button = 'audio\\effects\\check_button.ogg'
jump = 'audio\\effects\\jump.ogg'
stomp = 'audio\\effects\\stomp.ogg'
explosion = 'audio\\effects\\explosion.ogg'
game_over = 'audio\\effects\\game_over.ogg'

activate_button = pygame.mixer.Sound(activate_button)
activate_button.set_volume(1)

check_button = pygame.mixer.Sound(check_button)
check_button.set_volume(1)

jump = pygame.mixer.Sound(jump)
jump.set_volume(0.1)

stomp = pygame.mixer.Sound(stomp)
stomp.set_volume(1)

explosion = pygame.mixer.Sound(explosion)
explosion.set_volume(1)

game_over = pygame.mixer.Sound(game_over)
game_over.set_volume(0.5)

# Animation
jumping = [  # Jumping animation
    'graphics\\character\\jump\\1.png',
]

falling = [  # Falling animation
    'graphics\\character\\fall\\2.png',
    'graphics\\character\\fall\\3.png',
    'graphics\\character\\fall\\4.png',
    'graphics\\character\\fall\\5.png',
]

bonus_explosion = [  # Bonus explosion animation
    'graphics\\bonus\\explosion\\1.png',
    'graphics\\bonus\\explosion\\2.png',
    'graphics\\bonus\\explosion\\3.png',
    'graphics\\bonus\\explosion\\4.png',
    'graphics\\bonus\\explosion\\5.png',
    'graphics\\bonus\\explosion\\6.png',
]

# Images
# For gameplay
background_image = 'graphics\\background\\background.png'
bonus_default_image = 'graphics\\bonus\\defaultsituation\\power_keg_with_m.png'
platform_image = 'graphics\\platform\\normal\\platform.png'
broken_platform_image = 'graphics\\platform\\broken\\broken-platform.png'

# For the main menu
main_menu_background = 'graphics\\main_menu\\background\\background.png'
exit_button_non_active = 'graphics\\main_menu\\button\\non_active\\exit_btn.png'
start_button_non_active = 'graphics\\main_menu\\button\\non_active\\start_btn.png'
exit_button_active = 'graphics\\main_menu\\button\\active\\exit_btn.png'
start_button_active = 'graphics\\main_menu\\button\\active\\start_btn.png'
marwin_image = 'graphics\\main_menu\\marwin.png'

# For the game over and pause menus
game_over_image = 'graphics\\game_over_menu\\game_over.png'
restart_button_non_active = 'graphics\\game_over_menu\\buttons\\non_active\\restart.png'
mainmenu_button_non_active = 'graphics\\game_over_menu\\buttons\\non_active\\main_menu.png'
resume_button_non_active = 'graphics\\pause\\buttons\\non_active\\resume.png'
restart_button_active = 'graphics\\game_over_menu\\buttons\\active\\restart.png'
mainmenu_button_active = 'graphics\\game_over_menu\\buttons\\active\\main_menu.png'
resume_button_active = 'graphics\\pause\\buttons\\active\\resume.png'

# UI
frame_image_score = 'graphics\\UI\\frame.png'
frame_image_pause = 'graphics\\pause\\frame.png'

# Icon
icon = 'graphics\\UI\\m.png'
