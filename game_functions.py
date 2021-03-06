import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from scoreboard import Scoreboard
from random import randint
def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	if event.key == pygame.K_UP:
		ship.moving_up = True
	if event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()
def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False
	if event.key == pygame.K_UP:
		ship.moving_up = False
	if event.key == pygame.K_DOWN:
		ship.moving_down = False
def check_events(ai_settings,screen,stats,sb,play_button,ship,bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,mouse_x,mouse_y)
def check_play_button(ai_settings,screen,stats,sb,play_button,mouse_x,mouse_y):
	if play_button.rect.collidepoint(mouse_x,mouse_y):
		stats.game_active = True
		sb.prep_ships()
def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)
def update_bullets(ai_settings,screen,ship,aliens,bullets):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)
def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
	if stats.ship_left > 0:
		stats.ship_left -=1
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		sleep(0.5)
	else:
		stats.game_active = False
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		ai_settings.alien_speed_factor = 1
		stats.ship_left = 2
		ship.center_ship()
		sb.prep_ships()
def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
	check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)
def create_fleet(ai_settings,screen,ship,aliens):
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	number_alien_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_alien_x):
			creat_alien(ai_settings,screen,aliens,alien_number,row_number)
def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
			break
def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.fleet_drop_speed+=1
		ai_settings.alien_speed_factor+=0.5
		create_fleet(ai_settings,screen,ship,aliens)
def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
def change_fleet_direction(ai_settings,aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	random_number = randint(-25,25)
	alien.x = alien_width + 2 * alien_width * alien_number + random_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height+2*alien.rect.height * row_number
	aliens.add(alien)
def get_number_aliens_x(ai_settings,alien_width):
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_alien_x = int(available_space_x/(2*alien_width))
	return number_alien_x
	
def get_number_rows(ai_settings,ship_height,alien_height):
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()