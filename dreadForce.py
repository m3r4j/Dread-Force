import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

font = pygame.font.SysFont(None, 40)

black = (0, 0, 0)
text_colour = (255, 255, 0)

width, height = 800, 500

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('DreadForce')

game_icon = pygame.image.load('icon.png')

pygame.display.set_icon(game_icon)

fps = 60

floor = 345 # THIS IS THE FLOOR FOR THE CHARACTER

clock = pygame.time.Clock()

player_cooldown = 10


player_right = []
player_left = []

player_width = 70
player_height = 70

game_background = pygame.image.load('sprites/background.jpg')
game_background = pygame.transform.scale(game_background, (width, height))

flag_1 = pygame.image.load('sprites/flag_1.png')
flag_1 =  pygame.transform.scale(flag_1, (100, 100))

flag_2 = pygame.image.load('sprites/flag_2.png')
flag_2 =  pygame.transform.scale(flag_2, (100, 140))
flag_2 = pygame.transform.flip(flag_2, True, False)

bullet = pygame.image.load('sprites/bullet.png')

bullet_width = 18
bullet_height = 18


bullet_right = pygame.transform.scale(bullet, (bullet_width, bullet_height))
bullet_left = pygame.transform.rotate(bullet_right, 180) # TURN THE BULLET TO THE LEFT

nuke_width = 80
nuke_height = 50

nuke_img = pygame.image.load('sprites/nuke.png')
nuke_img = pygame.transform.rotate(nuke_img, 270)
nuke_img = pygame.transform.scale(nuke_img, (nuke_width, nuke_height))


def draw_flag_1():
	window.blit(flag_1, (10, 315))


def draw_flag_2():
	window.blit(flag_2, (width - 100, 296))

enemy_x = width - 100
enemy_y = 345



def generate_nuke():
	global nukes

	if len(nukes) == 0:
		nuke_rect = pygame.Rect(nuke_x, nuke_y, nuke_width, nuke_height)
		nukes.append(nuke_rect)


def draw_nukes():
	global nukes, explosion, nuke_x, nuke_y, enemies, kills

	for rect in nukes:
		window.blit(nuke_img, (rect.x, rect.y))

		if rect.y > floor + 22:
			if rect in nukes:
				nuke_x = rect.x
				nuke_y = rect.y

				nukes.remove(rect)
				explosion = True
				sounds.bomb()
				kills += len(enemies)

				if len(enemies) > 0:
					sounds.kill()

				enemies = []


		rect.y += 2.5

class sounds:
	def shoot():
		shoot_sound = pygame.mixer.Sound('audio/shoot.wav')
		shoot_sound.set_volume(0.3)
		pygame.mixer.Channel(0).play(shoot_sound)

	def nuke():
		nuke_sound = pygame.mixer.Sound('audio/nuke.wav')
		nuke_sound.set_volume(0.5)
		pygame.mixer.Channel(1).play(nuke_sound)

	def jump():
		jump_sound = pygame.mixer.Sound('audio/jump.wav')
		jump_sound.set_volume(0.3)
		pygame.mixer.Channel(2).play(jump_sound)

	def bomb():
		bomb_sound = pygame.mixer.Sound('audio/explosion.wav')
		bomb_sound.set_volume(0.5)
		pygame.mixer.Channel(3).play(bomb_sound)

	def dead():
		die_sound = pygame.mixer.Sound('audio/die.wav')
		die_sound.set_volume(0.4)
		pygame.mixer.Channel(4).play(die_sound)

	def kill():
		kill_sound = pygame.mixer.Sound('audio/kill.wav')
		kill_sound.set_volume(0.3)
		pygame.mixer.Channel(5).play(kill_sound)

	def shotgun():
		shotgun_sound = pygame.mixer.Sound('audio/shotgun.wav')
		shotgun_sound.set_volume(0.4)
		pygame.mixer.Channel(6).play(shotgun_sound)

	def round_over():
		round_sound = pygame.mixer.Sound('audio/round_over.wav')
		round_sound.set_volume(0.3)
		pygame.mixer.Channel(7).play(round_sound)

	def game_over():
		game_over_sound = pygame.mixer.Sound('audio/game_over.wav')
		game_over_sound.set_volume(0.9)
		pygame.mixer.Channel(7).play(game_over_sound)


def draw_background():
	window.blit(game_background, (0, 0))

for chars in range(1, 5):
	right_img = pygame.image.load(f'sprites/player_{chars}.png')
	right_img = pygame.transform.scale(right_img, (player_width, player_height))
	left_img = pygame.transform.flip(right_img, True, False)

	player_right.append(right_img)
	player_left.append(left_img)

player_speed = 7

bullet_speed = 9





def draw_bullets_right():
	global enemies, bullets_right, kills

	for rect in bullets_right:
		window.blit(bullet_right, (rect.x, rect.y))

		if rect.x > width + bullet_width:
			if rect in bullets_right:
				bullets_right.remove(rect)


		for i in enemies:
			if rect.colliderect(i):
				sounds.kill()
				if i in enemies:
					enemies.remove(i)

				if rect in bullets_right:
					bullets_right.remove(rect)

				kills += 1

		rect.x += bullet_speed

def draw_bullets_left():
	global enemies, bullets_left, kills

	for rect in bullets_left:
		window.blit(bullet_left, (rect.x, rect.y))

		if rect.x < -bullet_width:
			if rect in bullets_left:
				bullets_left.remove(rect)

		for i in enemies:
			if rect.colliderect(i):
				sounds.kill()
				if i in enemies:
					enemies.remove(i)

				if rect in bullets_left:
					bullets_left.remove(rect)

				kills += 1

		rect.x -= bullet_speed

def draw_player():
	if player_direction == 1: # RIGHT
		window.blit(player_right[player_index], (player_x, player_y))

	if player_direction == -1: # LEFT
		window.blit(player_left[player_index], (player_x, player_y))


def handle_player():
	global player_direction, player_x

	if keys[pygame.K_d] and not player_x + player_speed > width - player_width:
		player_direction = 1
		player_x += player_speed

	if keys[pygame.K_a] and not player_x < 10:
		player_direction = -1
		player_x -= player_speed


def draw_helicopter():
	global helicopter_x, helicopter_direction


	if helicopter_direction == 1:
		window.blit(helicopter_left[helicopter_index], (helicopter_x, helicopter_y))

	if helicopter_direction == -1:
		window.blit(helicopter_right[helicopter_index], (helicopter_x, helicopter_y))

	if helicopter_direction == 1:
		helicopter_x += helicopter_speed

	if helicopter_direction == -1:
		helicopter_x -= helicopter_speed

	if helicopter_x > width:
		helicopter_direction = -1

	if helicopter_x < -helicopter_width:
		helicopter_direction = 1

helicopter_right = []
helicopter_left = []

helicopter_width = 250
helicopter_height = 100

for i in range(1, 5):
	helicopter_left_img = pygame.image.load(f'sprites/helicopter_{i}.png')
	helicopter_left_img = pygame.transform.scale(helicopter_left_img, (helicopter_width, helicopter_height))

	helicopter_right_img = pygame.transform.flip(helicopter_left_img, True, False)

	helicopter_right.append(helicopter_right_img)
	helicopter_left.append(helicopter_left_img)


helicopter_cooldown = 3

helicopter_speed = 5

gravity = 0.50
jump_force_reset = 11


def handle_jump():
	global player_y, player_jumped, jump_force

	# CALCULATE THE JUMP STOP VALUE FOR A GIVEN JUMP FORCE SO YOU KNOW WHEN TO STOP
	jump_stop = jump_force_reset + gravity
	jump_stop = -jump_stop

	if player_jumped:
		player_y -= jump_force
		jump_force -= gravity


	if jump_force == jump_stop:
		player_jumped = False
		jump_force = jump_force_reset


def draw_explosion():
	global explosion_counter

	if explosion:
		window.blit(fire[explosion_index], (nuke_x - 200, nuke_y - 425))
		explosion_counter += 1



nuke_cooldown = 250

fire = []
explosion_cooldown = 3

fire_width = 500
fire_height = 500

for i in range(1, 25):
	fire_img = pygame.image.load(f'sprites/fire_{i}.png')
	fire_img = pygame.transform.scale(fire_img, (fire_width, fire_height))
	fire.append(fire_img)

enemy_width = 70
enemy_height = 70

enemy = []

laser_speed = 10

enemy_cooldown = 5


for i in range(1, 10):
	enemy_img = pygame.image.load(f'sprites/enemy_{i}.png')
	enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
	enemy_img = pygame.transform.flip(enemy_img, True, False)

	enemy.append(enemy_img)

def generate_enemies():
	global enemies

	if len(enemies) < max_enemies:
		enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
		enemies.append(enemy_rect)


def draw_enemies():
	global lasers, player_health, player_x, enemies

	for rect in enemies:
		window.blit(enemy[enemy_index], (rect.x, rect.y))
		rect.x -= enemy_speed

		if random.random() < shoot_rarity:
			enemy_laser_x = rect.x - 45
			enemy_laser_y = rect.y + 23
			laser_rect = pygame.Rect(enemy_laser_x, enemy_laser_y, laser_width, laser_height)
			lasers.append(laser_rect)
			sounds.shotgun()
			#window.blit(laser, (enemy_laser_x, enemy_laser_y))

		if rect.x <= 0:
			if rect in enemies:
				enemies.remove(rect)


def draw_lasers():
	global lasers, player_health

	for rect in lasers:
		window.blit(laser, (rect.x, rect.y))
		rect.x -= laser_speed

		if rect.x < 0:
			if rect in lasers:
				lasers.remove(rect)


		if rect.colliderect(player_rect):
			player_health -= 10
			sounds.dead()

			if rect in lasers:
				lasers.remove(rect)



laser_width = 50
laser_height = 10

laser = pygame.image.load('sprites/enemy_bullet.png')
laser = pygame.transform.scale(laser, (laser_width, laser_height))

text_y = 465

shoot_rarity_add = 0.001

def draw_health():
	text = font.render(f'HEALTH: {player_health}', True, text_colour)
	window.blit(text, (0, text_y))

def draw_rounds():
	text = font.render(f'ROUND: {round_num}', True, text_colour)
	window.blit(text, (300, text_y))


def draw_kills():
	text = font.render(f'KILLS: {kills}', True, text_colour)
	window.blit(text, (width - 200, text_y))




def check_health():
	if player_health <= 0:
		pygame.mixer.init()
		sounds.game_over()
		pygame.display.update()
		game_loop()


def check_rounds():
	global round_num, amount_of_kills, max_bullets, max_enemies, enemy_speed, player_health, shoot_rarity, nuke_ready

	if kills >= amount_of_kills:
		round_num += 1

		if random.random() < 0.01:
			max_bullets += 1

		max_enemies += 1
		amount_of_kills += 5
		enemy_speed += 0.25
		player_health += 1
		shoot_rarity += shoot_rarity_add
		#nuke_ready = True
		print(True)
		sounds.round_over()


def game_loop():
	global max_enemies, amount_of_kills, enemy_speed, player_health, shoot_rarity, max_bullets, kills, nuke_ready, round_num, lasers, explosion_counter, player_direction, player_index, player_x, player_y, bullets_right, bullets_left, helicopter_direction, helicopter_index, helicopter_x, helicopter_y, nukes, player_jumped, jump_force, explosion, enemies, keys, enemy_index, player_rect, nuke_x, nuke_y, explosion_index

	player_index = 0
	player_counter = 0
	player_direction = 1

	max_bullets = 2 # MAX BULLETS THAT CAN BE SHOT

	player_x = 100
	player_y = 345

	player_health = 100

	bullets_right = []
	bullets_left = []

	jump_force = jump_force_reset

	nukes = []

	explosion_counter = 0

	explosion = False
	explosion_index = 0

	enemy_index = 0
	enemy_speed = 0.1

	max_enemies = 1

	enemies = []
	lasers = []
	enemy_counter = 0
	helicopter_direction = 1
	helicopter_index = 0
	helicopter_counter = 0

	helicopter_x = 50
	helicopter_y = 25

	round_num = 1

	amount_of_kills = 5
	kills = 0

	nuke_ready = False

	shoot_rarity = 0.005

	player_jumped = False

	nuked = False
	nuke_counter = 0

	nuke_rarity = 0.0003

	show_stats = False

	while True:
		clock.tick(fps)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONUP:
				if len(bullets_right) < max_bullets and len(bullets_left) < max_bullets: # LESS THAN BECAUSE THE BULLETS LIST STARTS AT 0

					if player_direction == 1:
						bullet_x = player_x + 50
						bullet_y = player_y + 33
						bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
						bullets_right.append(bullet_rect)

					if player_direction == -1:
						bullet_x = player_x
						bullet_y = player_y + 36
						bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
						bullets_left.append(bullet_rect)

					sounds.shoot()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if player_jumped == False:
						player_jumped = True
						sounds.jump()

				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit()

				if event.key == pygame.K_1:
					show_stats = not show_stats

				#if event.key == pygame.K_c:
					#nuked = True

		keys = pygame.key.get_pressed()
		window.fill(black)


		# HELICOPTER ANIMATION
		if helicopter_counter > helicopter_cooldown:
			if helicopter_index >= len(helicopter_right) - 1:
				helicopter_index = 0

			helicopter_index += 1
			helicopter_counter = 0


		# PLAYER ANIMATION
		if player_counter > player_cooldown:
			if player_index >= len(player_right) - 1:
				player_index = 0

			player_index += 1
			player_counter = 0

		player_counter += 1
		helicopter_counter += 1
		enemy_counter += 1



		# NUKE
		if random.random() < nuke_rarity or nuke_ready: # CHECK FOR A RANDOM TIME TO SPAWN A NUKE
			if nuked == False and len(nukes) == 0 and explosion == False:
				sounds.nuke()
				nuke_ready = True
				nuked = True

		if nuked: # CHECK IF THEIR HAS BEEN A NUKE
			nuke_x = helicopter_x
			nuke_y = helicopter_y
			nuke_counter += 1

		if nuke_counter > nuke_cooldown and nuke_x > 50 < width - 150 and nuked: # CHECK THE COOLDOWN OF THE NUKE
			generate_nuke() # GENERATE A NUKE
			nuke_counter = 0
			nuked = False # LET THE PROGRAM KNOW THE NUKE FINISHED


		if explosion_counter > explosion_cooldown:
			if explosion_index >= len(fire) - 1:
				explosion_index = 0
				explosion_counter = 0
				explosion = False
				nuke_ready = False


			explosion_index += 1
			explosion_counter = 0


		if enemy_counter > enemy_cooldown:
			if enemy_index >= len(enemy) - 1:
				enemy_index = 0

			enemy_counter = 0
			enemy_index += 1

		player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

		# MAIN FUNCTIONS
		draw_background()
		draw_flag_1()
		draw_flag_2()
		draw_player()
		draw_bullets_right()
		draw_bullets_left()
		draw_helicopter()
		draw_nukes()
		handle_jump()
		draw_explosion()

		if random.random() < 0.01:
			generate_enemies()

		draw_enemies()
		draw_lasers()

		if show_stats:
			draw_health()
			draw_rounds()
			draw_kills()

		check_rounds()
		check_health()
		handle_player()

		pygame.display.update()

game_loop()
