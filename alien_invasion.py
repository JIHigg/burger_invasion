import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():

	# Initialize game and create a screen object.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))

	pygame.display.set_caption("Alien Invasion")
	
	#Make a ship, Group for bullets, and Group for aliens
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	#Create Stats instance and Scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#Create Play Button
	play_btn = Button(ai_settings, screen, 'Play')
	
	#Create fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)

	#Start the main loop for the game
	while True:
		
		gf.check_events(ai_settings, screen, stats, sb, play_btn, ship,
			bullets, aliens)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
			
		gf.update_screen(ai_settings, screen, sb, ship, stats, aliens, bullets,
				play_btn)
		
		
run_game()
