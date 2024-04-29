import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)

#load images
#background image
background_img = pygame.image.load('img/Background/background_img.jpg').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
#button images
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
#sword image
sword_image = pygame.image.load('img/Icons/sword.png').convert_alpha()


#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))


#function for drawing panel
def draw_panel():
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	#show knight stats
	draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
	for count, i in enumerate(monster_list):
		#show name and health
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)



#fighter class
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0 #0=idle 1=attack 2=hurt 3=dead
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width () * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width () * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load hurt images
		temp_list = []
		for i in range(3):
			img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width () * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load dead images
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width () * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		animation_cooldown = 100
		#handle animation & update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		# if the animation has run out then reset to the first frame
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()


	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()



	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		#run hurt animation
		target.hurt()
		#check if target is dead
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def hurt(self):
		#set variables to hurt animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to hurt animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def reset (self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()


	def draw(self):
		screen.blit(self.image, self.rect)



class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp

	def  draw(self, hp):
		#update health
		self.hp = hp
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, color):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, color)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0



	def update(self):
		#move damage text up after appearance
		self.rect.y -= 1
		self.counter += 1
		if self.counter > 30:
			self.kill()


damage_text_group = pygame.sprite.Group()






knight = Fighter(200, 340, 'Knight', 30, 10, 3)
monster1 = Fighter(400, 300, 'Monster', 20, 6, 1)
monster2 = Fighter(625, 300, 'Monster', 20, 6, 1)

monster_list = []
monster_list.append(monster1)
monster_list.append(monster2)


knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
monster1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, monster1.hp, monster1.max_hp)
monster2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, monster2.hp, monster2.max_hp)


#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	knight_health_bar.draw(knight.hp)
	monster1_health_bar.draw(monster1.hp)
	monster2_health_bar.draw(monster2.hp)

	#draw fighters
	knight.update()
	knight.draw()
	for monster in monster_list:
		monster.update()
		monster.draw()


	#draw damage text
	damage_text_group.update()
	damage_text_group.draw(screen)


	#player actions
	#reset action variables
	attack = False
	potion = False
	target = None
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, monster in enumerate(monster_list):
		if monster.rect.collidepoint(pos):
			pygame.mouse.set_visible(False)
			#show sword in place of mouse cursor
			screen.blit(sword_image, pos)
			if clicked == True and monster.alive == True:
				attack = True
				target = monster_list[count]
		if potion_button.draw():
			potion = True
		#show number of potions
		draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)

	if game_over == 0:
		#player action
		if knight.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					if attack == True and target != None:
						knight.attack(target)
						current_fighter += 1
						action_cooldown = 0
					#potion
					if potion == True:
						if knight.potions > 0:
							#check if the potion would heal the player beyond max health
							if knight.max_hp - knight.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = knight.max_hp - knight.hp
							knight.hp += heal_amount
							knight.potions -= 1
							damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0
		else: 
			game_over = -1

		#enemy action
		for count, monster in enumerate(monster_list):
			if current_fighter == 2 + count:
				if monster.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
						#check if monster needs to heal
						if (monster.hp / monster.max_hp) < 0.5 and monster.potions > 0:
						#check if the potion would heal the monster beyond max health
								if monster.max_hp - monster.hp > potion_effect:
										heal_amount = potion_effect
								else:
									heal_amount = monster.max_hp - monster.hp
								monster.hp += heal_amount
								monster.potions -= 1
								damage_text = DamageText(monster.rect.centerx, monster.rect.y, str(heal_amount), green)
								damage_text_group.add(damage_text)
								current_fighter += 1
								action_cooldown = 0

						#attack
						else: 
							monster.attack(knight)
							current_fighter += 1
							action_cooldown = 0  
				else:
					current_fighter += 1


		#if all fighters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1



#check if all monsters are dead
	alive_monsters = 0
	for monster in monster_list:
		if monster.alive == True:
			alive_monsters += 1
	if alive_monsters == 0:
		game_over = 1



	#check if game is over
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
		if restart_button.draw():
			knight.reset()
			for monster in monster_list:
				monster.reset()
			current_fighter = 1
			action_cooldown
			game_over = 0


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()

pygame.quit()