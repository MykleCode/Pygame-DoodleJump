from random import randint 
from pygame import Surface, image, transform, mixer
from pygame.time import Clock, get_ticks
import asyncio
import settings as config
from singleton import Singleton
from sprite import Sprite
mixer.init()

chance = lambda x: not randint(0,x) # Creating a variable dependent on x, the more x, the less likely it is to get True
class Bonus(Sprite):
	def __init__(self, parent:Sprite, force=config.PLAYER_BONUS_JUMPFORCE): # Accepting the parameters of the parent object
		self.parent = parent # Binding
		super().__init__(*self._get_inital_pos(),
			config.BONUS_WIDTH, config.BONUS_HEIGHT) # Position, width, height, color are passed
		self.force = force # Jump power
		self.model = image.load(config.bonus_default_image).convert_alpha() # Image model
		self.effect = False # If player speed increase effect occurs (used to start animation)
		self.tag = 'bonus' # tag
		self.bonus_effect_duration = 100 # Bonus animation effect duration
		self.bonus_effect_start_time = None # Blank for counting the start of the animation
		self.current_frame = 0 # Current animation frame
		self.animation_finished = False # Animation ended
	
	def _get_inital_pos(self):
		# Getting the current position
		x = self.parent.rect.centerx - config.BONUS_WIDTH//2
		y = self.parent.rect.y - config.BONUS_HEIGHT
		return x,y
	
class Platform(Sprite):
	def __init__(self, x:int, y:int, width:int, height:int,
			initial_bonus=False,breakable=False): # designation of data types and initial parameters in the class constructor
		self.model = image.load(config.platform_image).convert_alpha() # model (default)
		self.tag = 'platform' # tag

		if breakable: # Model change if the platform is disposable
			self.model = image.load(config.broken_platform_image).convert_alpha() # model (broken)
		
		super().__init__(x,y,width,height)
		self.breakable = breakable 
		self.__level = Level.instance # Setting value equal to class instance Level
		self.__bonus = None # Blank for creating a personal instance of the Bonus class
		if initial_bonus: # If the platform have a bonus 
			self.add_bonus(Bonus) # Adding in a sprite group

	@property # The ability to open access the class
	def bonus(self): 
		return self.__bonus

	def add_bonus(self,bonus_type:type):
		# Adds a bonus to the platform
		assert issubclass(bonus_type,Bonus) # Checking if bonus_type is a subclass of Bonus
		if not self.__bonus and not self.breakable: # Checking whether there is already a bonus on the platform and whether it is a solid platform
			self.__bonus = bonus_type(self) # If the conditions match, a bonus instance of type bonus_type is created
	
	def remove_bonus(self):
		self.__bonus = None

	def onCollide(self):
		# Removal of the platform if it is a one-time use
		if self.breakable:
			config.stomp.play() # Breaking sound production
			self.__level.remove_platform(self)
		
	def draw(self, surface:Surface):
		# Rendering the platform on the passed Surface
		super().draw(surface) # Draw method call
		distance = 0
		if self.__bonus: # Checking for the existence of an object on the platform
			self.__bonus.draw(surface) 
			distance = config.BONUS_HEIGHT # Bonus amount
		if self.camera_rect.y + self.rect.height > config.YWIN + distance + 5:  # Checking if the platform boundary goes beyond the screen
			self.__level.remove_platform(self) # Removing a platform

class Level(Singleton):
	def __init__(self):
		self.platform_size = config.PLATFORM_SIZE # Platform size
		self.max_platforms = config.MAX_PLATFORM_NUMBER # Max platform count
		self.distance_min = min(config.PLATFORM_DISTANCE_GAP) # Minimum distance between platforms
		self.distance_max = max(config.PLATFORM_DISTANCE_GAP) # Maximum distance between platforms


		self.bonus_platform_chance = config.BONUS_SPAWN_CHANCE # Bonus spawn chance
		self.breakable_platform_chance = config.BREAKABLE_PLATFORM_CHANCE # Disposable platform chance

		self.__platforms = [] 
		self.__to_remove = [] # Whatever needs to be removed
		
		# Creating a platform instance
		self.__base_platform = Platform( 
			config.HALF_XWIN - self.platform_size[0]//2, # X pos
			config.HALF_YWIN + config.YWIN/3, # Y pos
			*self.platform_size) # Size

	# Definition as a class property
	@property
	def platforms(self) -> list: # Expected data type: list
		return self.__platforms # Returns all platforms as list

	# Asynchronous function (asynchrony is used to optimize and process the function by several processor cores)
	async def _generation(self): 
		# Checking the required number of platforms for generation
		nb_to_generate = self.max_platforms - len(self.__platforms) # Calculation of the number of platforms for generation
		for _ in range(nb_to_generate): # Creating a platforms
			self.create_platform()
		
	def create_platform(self):
		# Creating a new platforms
		if self.__platforms: # If platform exists
			# Generation a random platform 
			offset = randint(self.distance_min,self.distance_max) # Mixing relative to neighbors
			self.__platforms.append(Platform( # Creating a new instance
				randint(0,config.XWIN-self.platform_size[0]), # X pos
				self.__platforms[-1].rect.y-offset, # Y pos
				*self.platform_size, # Size
				initial_bonus=chance(self.bonus_platform_chance), # Bonus available
				breakable=chance(self.breakable_platform_chance))) # Disposable or not
		else:
			# If the platform does not exist, adds the base platform to the list
			self.__platforms.append(self.__base_platform)

	def remove_platform(self,plt:Platform) -> bool: # Return value bool
		if plt in self.__platforms:
			self.__to_remove.append(plt)
			return True
		return False # Platform has not found

	def reset(self):
		# Platform reloading, by assigning platforms to one base platform
		self.__platforms = [self.__base_platform]

	def update(self):
		# Called every frame to generate
		for platform in self.__to_remove:
			if platform in self.__platforms:
				self.__platforms.remove(platform)
		self.__to_remove = []
		asyncio.run(self._generation()) # Running a function using async

	def draw(self,surface:Surface):
		for platform in self.__platforms: # Rendering of each platform
			platform.draw(surface) 
