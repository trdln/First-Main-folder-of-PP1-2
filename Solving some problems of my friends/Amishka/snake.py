import pygame, os, sys
import random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
fps = 30
surface = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Simple Snake game")

font = pygame.font.Font(None, 32)

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class GameData:

	def __init__(self):
		self.lives = 3
		self.isDead = False
		self.blocks = []
		self.tick = 250
		self.speed = 250
		self.level = 1
		self.berrycount = 0
		self.segments = 1
		self.frame = 0
		if self.level==1:
			bx = random.randint(1, 38)
			by = random.randint(1, 28)
		elif self.level==2:
			z=random.randint(1, 5)
			if z==1:
				bx = random.randint(1, 11)
				by = random.randint(1, 28)
			elif z==2:
				bx = random.randint(27, 38)
				by = random.randint(1, 28)
			elif z==3:
				bx = random.randint(12, 26)
				by = random.randint(1, 4)
			elif z==4:
				bx = random.randint(12, 26)
				by = random.randint(6, 23)
			elif z==5:
				bx = random.randint(12, 26)
				by = random.randint(25, 28)
		elif self.level>=3:
			l=random.randint(1, 8)
			if l==1:
				bx = random.randint(1, 11)
				by = random.randint(1, 28)
			elif l==2:
				bx = random.randint(27, 38)
				by = random.randint(1, 28)
			elif l==3:
				bx = random.randint(12, 26)
				by = random.randint(1, 4)
			elif l==4:
				bx = random.randint(12, 26)
				by = random.randint(6, 11)
			elif l==5:
				bx = random.randint(13, 25)
				by = random.randint(12, 13)
			elif l==6:
				bx = random.randint(13, 25)
				by = random.randint(15, 16)
			elif l==7:
				bx = random.randint(12, 26)
				by = random.randint(17, 23)
			elif l==8:
				bx = random.randint(12, 26)
				by = random.randint(25, 28)
		self.berry = Position(bx, by)
		self.blocks.append(Position(20,15))
		self.blocks.append(Position(19,15))
		self.direction = 0 # 0 = right, 1 = left, 2 = up, 3 = down

def loseLife(gamedata):
	gamedata.lives -= 1
	gamedata.direction = 0
	gamedata.blocks[:] = []
	gamedata.blocks.append(Position(20,15))
	gamedata.blocks.append(Position(19,15))

def positionBerry(gamedata):
	bx = random.randint(1, 38)
	by = random.randint(1, 28)
	found = True
	
	while (found):
		found = False
		for b in gamedata.blocks:
			if (b.x == bx and b.y == by):
				found = True
				
		if (found):
			bx = random.randint(1, 38)
			by = random.randint(1, 28)				
			
	gamedata.berry = Position(bx, by)


def loadMapFile(fileName):
	f = open(fileName, 'r')
	content = f.readlines()
	f.close()
	return content
	
def headHitBody(gamedata):
	head = gamedata.blocks[0]
	
	for b in gamedata.blocks:
		if (b != head):
			if(b.x == head.x and b.y == head.y):
				return True
				
	return False
	
def headHitWall(map, gamedata):
	row = 0

	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):	
				if (gamedata.blocks[0].x == col and gamedata.blocks[0].y == row):
					return True

			col += 1

		row += 1	
		
	return False

def drawData(surface, gamedata):
	text = font.render("Lives = %d, Level = %d" % ( gamedata.lives, gamedata.level ), 0, (255, 255, 255))
	textpos = text.get_rect(centerx=surface.get_width()/2, top=32)
	surface.blit(text, textpos)
	
def drawGameOver(surface):
	text1 = font.render("Game Over", 1, (255, 255, 255))
	text2 = font.render("Space to play or close the window", 1, (255, 255, 255))
	textpos1 = text1.get_rect(centerx=surface.get_width()/2, top=surface.get_height()/2 - 48)
	textpos2 = text2.get_rect(centerx=surface.get_width()/2, top=surface.get_height()/2)
	surface.blit(text1, textpos1)
	surface.blit(text2, textpos2)
	
	
def drawWalls(surface, img, map):

	row = 0

	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):
				imgRect = img.get_rect()
				imgRect.left = col * 16
				imgRect.top = row * 16
				surface.blit(img, imgRect)
			col += 1

		row += 1

def drawSnake(surface, img, gamedata):
	first = True

	for b in gamedata.blocks:
		dest = (b.x * 16, b.y * 16, 16, 16)
		if ( first ):
			first = False
			src = (((gamedata.direction * 2) + gamedata.frame) * 16, 0, 16, 16)
		else:
			src = (8 * 16, 0, 16, 16)

		surface.blit(img, dest, src)
		
def updateGame(gamedata, gameTime):
	gamedata.tick -= gameTime
	
	head = gamedata.blocks[0]
	
	if (gamedata.tick < 0):
		gamedata.tick += gamedata.speed
		gamedata.frame += 1
		gamedata.frame %= 2
		if (gamedata.direction == 0):
			move = (1, 0)
		elif (gamedata.direction == 1):
			move = (-1, 0)
		elif (gamedata.direction == 2):
			move = (0, -1)
		else:
			move = (0, 1)
			
		newpos = Position(head.x + move[0], head.y + move[1])
		
		first = True
		for b in gamedata.blocks:
			temp = Position(b.x, b.y)
			b.x = newpos.x
			b.y = newpos.y
			newpos = Position(temp.x, temp.y)			


	keys = pygame.key.get_pressed()
		
	# if gamedata==data:		
	if (keys[K_RIGHT] and gamedata.direction != 1):
		gamedata.direction = 0
	elif (keys[K_LEFT] and gamedata.direction != 0):
		gamedata.direction = 1
	elif(keys[K_UP] and gamedata.direction != 3):
		gamedata.direction = 2 
	elif(keys[K_DOWN] and gamedata.direction != 2):
		gamedata.direction = 3
	# else:
	# 	if (keys[K_d] and gamedata.direction != 1):
	# 		gamedata.direction = 0
	# 	elif (keys[K_a] and gamedata.direction != 0):
	# 		gamedata.direction = 1
	# 	elif(keys[K_w] and gamedata.direction != 3):
	# 		gamedata.direction = 2 
	# 	elif(keys[K_s] and gamedata.direction != 2):
	# 		gamedata.direction = 3
		
	
	if (head.x == gamedata.berry.x and head.y == gamedata.berry.y):
		lastIdx = len(gamedata.blocks) - 1
		for i in range(gamedata.segments):
			gamedata.blocks.append(Position(gamedata.blocks[lastIdx].x, gamedata.blocks[lastIdx].y))
	
		bx = random.randint(1, 38)
		by = random.randint(1, 28)
		gamedata.berry = Position(bx, by)
		gamedata.berrycount += 1
		if (gamedata.berrycount == 10):
			gamedata.berrycount = 0
			gamedata.speed -= 25
			gamedata.level += 1
			gamedata.segments *= 2
			if (gamedata.segments > 64):
				gamedata.segments = 64
			
			if (gamedata.speed < 100):
				gamedata.speed = 100

def loadImages():
	wall = pygame.image.load('wall.png')
	raspberry = pygame.image.load('berry.png')
	snake = pygame.image.load('snake.png')
	snake2 = pygame.image.load('snake2.png')
	
	return {'wall':wall, 'berry':raspberry, 'snake':snake, 'snake2':snake2}
	
	
images = loadImages()

images['berry'].set_colorkey((255, 0, 255))
snakemap = loadMapFile('map.txt')
snakemap2 = loadMapFile('map2.txt')
snakemap3 = loadMapFile('map3.txt')
data = GameData()
# data2 = GameData()
# data2.blocks[0]=(Position(15, 15))
# data2.blocks[1]=(Position(14,15))

quitGame = False
isPlaying = False

while not quitGame:

	if isPlaying:
		x = random.randint(1, 38)
		y = random.randint(1, 28)
	
		rrect = images['berry'].get_rect()
		rrect.left = data.berry.x * 16
		rrect.top = data.berry.y * 16
	
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	
		updateGame(data, fpsClock.get_time())
		# updateGame(data2, fpsClock.get_time())
		if data.level==1:
			fps=30
		elif data.level==2:
			fps=40
		elif data.level>=3:
			fps=50
		if data.level==1:
			crashed = headHitWall(snakemap, data) or headHitBody(data)
		elif data.level==2:
			crashed = headHitWall(snakemap2, data) or headHitBody(data)
		elif data.level>=3:
			crashed = headHitWall(snakemap3, data) or headHitBody(data)
		if (crashed):
			loseLife(data)
			positionBerry(data)
			
		isPlaying = (data.lives > 0) #and (data2.lives > 0)
		
		if (isPlaying):	
			surface.fill((0, 0, 0))
		
			if data.level==1:
				drawWalls(surface, images['wall'], snakemap)
			elif data.level==2:
				drawWalls(surface, images['wall'], snakemap2)
			elif data.level>=3:
				drawWalls(surface, images['wall'], snakemap3)
			surface.blit(images['berry'], rrect)
			drawSnake(surface, images['snake'], data)
			# drawSnake(surface, images['snake2'], data2)
			drawData(surface, data)
	else:
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		if (keys[K_SPACE]):
			isPlaying = True
			data = None
			data = GameData()
			
		drawGameOver(surface)

	pygame.display.update()
	fpsClock.tick(fps)