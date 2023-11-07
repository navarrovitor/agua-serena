import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')


#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)


#define game variables
tile_size = 50
game_over = 0
main_menu = False
level = 7
max_levels = 8
score = 0


#define colours
white = (255, 255, 255)
blue = (0, 0, 255)


#load images

sun_img = pygame.image.load('./jogo/img/sun.png')
restart_img = pygame.image.load('./jogo/img/restart_btn.png')
start_img = pygame.image.load('./jogo/img/start_btn.png')
shrek_img = pygame.image.load('./jogo/img/shrek.jpg')
exit_img = pygame.image.load('./jogo/img/exit_btn.png')
exit_img = pygame.transform.scale(exit_img, (100, 50))

#load sounds
pygame.mixer.music.load('./jogo/img/music.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
pygame.mixer.music.set_volume(0.5)
coin_fx = pygame.mixer.Sound('./jogo/img/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('./jogo/img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('./jogo/img/game_over.wav')
game_over_fx.set_volume(0.5)
shrek_fx = pygame.mixer.Sound('./jogo/img/shrek.mp3')
shrek_fx.set_volume(0.5)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#function to reset level
def reset_level(level):
	player.reset(100, screen_height - 130)
	blob_group.empty()
	water_group.empty()
	exit_group.empty()

	#load in level data and create world
	if path.exists(f'./jogo/level{level}_data'):
		pickle_in = open(f'./jogo/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)

	return world


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action


class Player():
	def __init__(self, x, y):
		self.reset(x, y)



	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
				game_over_fx.play()


			if pygame.sprite.spritecollide(self, water_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(0, 9):
			img_right = pygame.image.load(f'./jogo/img/bonecoM/walk{num}.png')
			img_right = pygame.transform.scale(img_right, (50, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('./jogo/img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True


class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		castleBlock_img = pygame.image.load('./jogo/img/castleBlock.png')
		castleBlock2_img = pygame.image.load('./jogo/img/castleBlock2.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(castleBlock_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(castleBlock2_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blob_group.add(blob)
				if tile == 6:
					water = Water(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					water_group.add(water)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('./jogo/img/blob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1

class Water(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('./jogo/img/water.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('./jogo/img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('./jogo/img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Scoreboard():
    def __init__(self, screen):
        self.screen = screen
        self.input_box = pygame.Rect(100, 200, 140, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.done = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self):
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)

	
	
player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world
if path.exists(f'./jogo/level{level}_data'):
	pickle_in = open(f'./jogo/level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)

#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width - 150, 0, exit_img)


background_images = {
    1: pygame.image.load('./jogo/backgrounds/bg1.jpg'),
    2: pygame.image.load('./jogo/backgrounds/bg2.jpg'),
	3: pygame.image.load('./jogo/backgrounds/bg3.jpg'),
	4: pygame.image.load('./jogo/backgrounds/bg4.jpg'),
	5: pygame.image.load('./jogo/backgrounds/bg5.jpg'),
	6: pygame.image.load('./jogo/backgrounds/bg6.jpg'),
	7: pygame.image.load('./jogo/backgrounds/bg7.jpg'),
	8: pygame.image.load('./jogo/backgrounds/bg8.jpg')
    # Add more levels as needed
}


run = True
scoreboard = Scoreboard(screen)
while run:

	clock.tick(fps)
	if level < max_levels:
		background = pygame.transform.scale(background_images[level], (screen_width, screen_height))
		screen.blit(background, (0, 0))
	else:
		screen.fill(white)


	world.draw()

	if game_over == 0:
		blob_group.update()
		#update score
		#check if a coin has been collected
		if pygame.sprite.spritecollide(player, coin_group, True):
			score += 1
			coin_fx.play()
		draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
	
	blob_group.draw(screen)
	water_group.draw(screen)
	coin_group.draw(screen)
	exit_group.draw(screen)

	game_over = player.update(game_over)

	if exit_button.draw():
		while not scoreboard.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					break
				scoreboard.handle_event(event)
			screen.fill(white)
			draw_text('Digite seu nome para salvar os pontos:', font, blue, 100, 100)
			scoreboard.draw()
			pygame.display.flip()
		if run:
			with open('./telaScoreboard/scores.csv', 'a') as file:
				file.write(f"{scoreboard.text},{score}\n")
			scoreboard = Scoreboard(screen)
			run = False

	#if player has died
	if game_over == -1:
		if restart_button.draw():
			world_data = []
			world = reset_level(level)
			game_over = 0
			score = 0

	#if player has completed the level
	if game_over == 1:
		#reset game and go to next level
		level += 1
		if level < max_levels:
			#reset level
			world_data = []
			world = reset_level(level)
			game_over = 0
		else:
			pygame.mixer.music.pause()
			shrek_fx.play()
			background = pygame.transform.scale(shrek_img, (screen_width, screen_height))
			screen.blit(background, (0, 0))
			draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
			if restart_button.draw():
				level = 1
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0
				shrek_fx.stop()
				pygame.mixer.music.unpause()



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()
