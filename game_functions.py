import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_events(ai_settings, screen, stats, sb, play_btn, ship, bullets,
		aliens):
	"""Respond to keypresses and mouse events."""
	#Watch for keyboard and mouse events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit() #Exit
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, sb, ship, aliens, bullets,
				stats, play_btn, mouse_x, mouse_y)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, sb, ship,
				bullets, stats, aliens)	#Move ship			
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship) #Stop ship
			
			
def check_play_button(ai_settings, screen, sb, ship, aliens, bullets, stats,
		play_btn, mouse_x, mouse_y):
	"""Start new game on Play Button click"""
	btn_clicked = play_btn.rect.collidepoint(mouse_x, mouse_y)
	if btn_clicked and not stats.game_active:
		start_game(ai_settings, screen, ship, stats, sb, bullets, aliens)
		

def start_game(ai_settings, screen, ship, stats, sb, bullets, aliens):
	"""Initiates new aliens, ship, and hides mouse for new game"""
	#Reset game settings
	ai_settings.initialize_dynamic_settings()
	
	#Hide mouse during gameplay
	pygame.mouse.set_visible(False)
		
	#Reset game statistics
	stats.reset_stats()
	stats.game_active = True
	
	#Reset scoreboard and level
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()
	
	#Empty aliens and bullets
	aliens.empty()
	bullets.empty()
		
	#Create new fleet and center ship
	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()

def check_keydown_events(event, ai_settings, screen, sb, ship, bullets,
	stats, aliens):
	"""Respond to keypresses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True #Move the ship to the right
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True #Move the ship left
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_p:
		start_game(ai_settings, screen, ship, stats, sb, bullets, aliens)
	elif event.key == pygame.K_q:
		sys.exit()
		
def check_keyup_events(event, ship):
	"""Respond to key releases"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False #Stops ship right
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False #Stops ship left

def update_screen(ai_settings, screen, sb, ship, stats, aliens, bullets, play_btn):
	"""Update images on the screen and flip to the new screen."""
	# Redraw screen each pass through the loop
	screen.fill(ai_settings.bg_color)
	# Redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	#Draw scoreboard
	sb.show_score()
	
	#Draw Play Button if the game is inactive
	if not stats.game_active:
		play_btn.draw_button()
				
	# Make the most recent screen visible
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Update position of bullets and remove old bullets"""
	#Update bullet positions
	bullets.update()
	
	#Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	#Check if any bullets hit any aliens
	check_bullet_alien_collisions(ai_settings, screen, stats, sb,
		ship, aliens, bullets)
	
	
def check_high_score(stats, sb):
	"""Check if there is a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
		ship, aliens, bullets):
	"""Respond to bullet-alien collisions"""
	#Detect collisions and remove sprites on collision
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points
			sb.prep_score()
		check_high_score(stats, sb)
			
	if len(aliens) == 0:
		#Start a new level
		bullets.empty()
		ai_settings.increase_speed()
		
		#Increase level
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)
		
		
def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Check if any alien reaches bottom of the screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#Same as if ship is hit
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break
			
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit is not reached"""
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship) #Create new bullet
		bullets.add(new_bullet)
		
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on screen"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height)
							- ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
		
def get_number_aliens_x(ai_settings, alien_width):
	"""Determine number of aliens that fit in a row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create ann alien and place it in the row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien) 
		
def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a fleet of aliens"""
	# Create an alien and find the number of aliens in a row.
	# Spacing between each alien is equal to one alien width.
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)
	
	#Create the fleet of aliens
	for row_number in range(number_rows): 
		for alien_number in range(number_aliens_x):
			#Create alien and put it in a row
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
			
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Check if the fleet is at an edge, then update positions of 
	all aliens in the fleet"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	# Detect alien+ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
		
	# Detect aliens at bottom of screen
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
	
	
def check_fleet_edges(ai_settings, aliens):
	"""Respond appropriately if any aliens reach an edge of screen"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Respond to ship being hit by alien"""
	if stats.ships_left > 0:
		
		#Decrement ships left
		stats.ships_left -= 1
		
		#Update scoreboard
		sb.prep_ships()
		
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
	
		#Create new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#Pause 
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
