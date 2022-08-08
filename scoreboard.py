import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	"""A class to report scoring information"""
	def __init__(self, ai_settings, screen, stats):
		"""Initialize scorekeeping attributes"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#Font settings for score settings
		self.text_color = (200, 200, 200)
		self.font = pygame.font.SysFont(None, 48)
		
		#Initial score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		
	def prep_ships(self):
		"""Shows how many ships are left"""
		self.ships = Group()
		for ship_num in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_num * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
		
	def prep_level(self):
		"""Render level as image"""
		self.level_str = "Lvl: " + str(self.stats.level)
		self.level_img = self.font.render(self.level_str, True, 
			self.text_color, self.ai_settings.bg_color)
			
		#Position level below score
		self.level_rect = self.level_img.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
		
	def prep_high_score(self):
		"""Render high score as image"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "High Score: " + "{:,}".format(high_score)
		self.high_score_img = self.font.render(high_score_str, True, 
			self.text_color, self.ai_settings.bg_color)
			
		#Center the high score at top of screen
		self.high_score_rect = self.high_score_img.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.screen_rect.top
		
	def prep_score(self):
		"""Render score into image"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "Score: " + "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color,
			self.ai_settings.bg_color)
			
		#Display the score in top right corner
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def show_score(self):
		"""Draw score and level to the screen"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_img, self.high_score_rect)
		self.screen.blit(self.level_img, self.level_rect)
		#Draw Ships
		self.ships.draw(self.screen)
