class Settings():
	"""A class to store all settings for Alien Invasion."""
	
	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (100,100,100)
		
		# Ship settings
		self.ship_limit = 3

		#Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 255,255,255
		self.bullets_allowed = 10

		#Alien settings
		self.fleet_drop_speed = 10
		
		#How quickly the game speeds up on level up
		self.speedup_scale = 1.1
		#Point increase scale
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize game settings that change throughout game"""
		self.ship_speed_factor = 2
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		
		# fleet_direction = 1 => Right; -1 => Left
		self.fleet_direction = 1
		
		#Scoring
		self.alien_points = 50
		
	def increase_speed(self):
		"""Increase speed and score values"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
