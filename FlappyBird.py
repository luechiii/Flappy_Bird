#Import Module pygame and random
import pygame
from pygame.locals import *
import random

#initialization module pygame
pygame.init()

#create clock varible and set fps to 60
clock = pygame.time.Clock()
fps = 60

#define windows size and set caption
window_width = 864
window_height = 936
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

#define funtion draw text for score
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	window.blit(img, (x, y))

#define function for reset button
def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(window_height / 2)
	score = 0
	return score

#define class bird
class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'img/bird{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):

		if flying == True:
			#gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			#jump
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			#handle the animation
			self.counter += 1
			flap_cooldown = 5
			#define animation speed
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			#rotate the bird
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			#define for game over
			self.image = pygame.transform.rotate(self.images[self.index], -90)

#define pipe class 
class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/pipe.png')
		self.rect = self.image.get_rect()
		#position 1 is from the top, -1 is from the bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]

	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()

#define class button
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		#check if mouse is over the button
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
		#draw button
		window.blit(self.image, (self.rect.x, self.rect.y))
		return action

#add groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

#set start coordinates
flappy = Bird(100, int(window_height / 2))

#add flapyy to bird_group
bird_group.add(flappy)

#create restart button instance
button = Button(window_width // 2 - 50, window_height // 2 - 100, button_img)

#create loof for the game
run = True
while run:
    #set fps
	clock.tick(fps)

	#draw background
	window.blit(bg, (0,0))

    #draw bird an pipe
	bird_group.draw(window)
	bird_group.update()
	pipe_group.draw(window)

	#draw the ground
	window.blit(ground_img, (ground_scroll, 768))

	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False

    #draw the score
	draw_text(str(score), font, white, int(window_width / 2), 20)

	#look for collision
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True

	#check if bird has hit the ground
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False

    #trigger only when note game over
	if game_over == False and flying == True:

		#generate new pipes
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(window_width, int(window_height / 2) + pipe_height, -1)
			top_pipe = Pipe(window_width, int(window_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now

		#draw and scroll the ground
		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0

        # update pipes
		pipe_group.update()


	#check for game over and reset
	if game_over == True:
		if button.draw() == True:
			game_over = False
			score = reset_game()

    # for loop to check events
	for event in pygame.event.get():
		#end when klick x
		if event.type == pygame.QUIT:
			run = False
        #start game when click mouse left
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

    #update game
	pygame.display.update()

pygame.quit()