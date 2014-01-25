from sys import exit
import pygame
import math
from pygame.locals import *

screenx = 1024
screeny = 768
framerate = 60
black = 0,0,0
white = 255,255,255
degs = math.pi / 180

stop_limit = 0.005  #when speed is less than this, ship stops
drag = 0.02      #should be less than 1!!!
accel = 0.12
turn = 0.3
debounce = 10
damper = True

bounce = 0

pygame.init()
screen = pygame.display.set_mode((screenx,screeny))
clock = pygame.time.Clock()

on = pygame.image.load('on.png')
on = pygame.transform.scale(on,(100,40))
off = pygame.image.load('off.png')
off = pygame.transform.scale(off,(100,40))

class Player(object):
	def __init__(self):
		self.sx = 200
		self.sy = 200
		self.vx = 0
		self.vy = 0
		self.angle = 0

player = Player()

pygame.key.set_repeat(1,1)

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	
	if player.angle > 180: player.angle = -180
	if player.angle < -180: player.angle = 180
	
	keys = pygame.key.get_pressed()
	
	if keys[K_LEFT]:
		player.angle -= 10 * turn
	if keys[K_RIGHT]:
		player.angle += 10 * turn
	if keys[K_UP]:
		player.vx += (math.cos((player.angle)*degs)) * accel
		player.vy += (math.sin((player.angle)*degs)) * accel
	if keys[K_DOWN]:
		print "\nVX: " + str(player.vx)
		print "VY: " + str(player.vy)
		vector = (math.atan(player.vy/player.vx))
		print "H:  " + str(vector*math.pi)
		print "A:  " + str(player.angle*degs)
	if keys[K_SPACE] and bounce == 0:
		damper = not(damper)
		bounce = debounce
		if damper:
			print "Inertial dampers ON"
		else:
			print "Intertial dampers OFF"
			
	
	if bounce > 0: bounce -= 1
		
	x = (math.cos(player.angle*degs))
	y = math.sin(player.angle*degs)
	point1 = ((10*x)+player.sx,(10*y)+player.sy)
	x = math.cos((player.angle+150)*degs)
	y = math.sin((player.angle+150)*degs)
	point2 = ((10*x)+player.sx,(10*y)+player.sy)
	x = math.cos((player.angle+210)*degs)
	y = math.sin((player.angle+210)*degs)
	point3 = ((10*x)+player.sx,(10*y)+player.sy)
	points = (point1, point2, point3)
	
	player.sx += player.vx
	player.sy += player.vy
	
	if (player.vx < stop_limit) and (player.vx > (- stop_limit)): player.vx = 0
	if (player.vy < stop_limit) and (player.vy > (- stop_limit)): player.vy = 0
	
	if damper:
		player.vx -= player.vx * drag
		player.vy -= player.vy * drag
	
	if player.sx > screenx: player.sx = 0
	if player.sy > screeny: player.sy = 0
	
	if player.sx < 0: player.sx = screenx
	if player.sy < 0: player.sy = screeny
	
	
	screen.fill(black)
	pygame.draw.polygon(screen, white, points, 1)
	
	if damper:
		screen.blit(on,(0,0))
	else:
		screen.blit(off,(0,0))
	
	clock.tick(60)
	
	pygame.display.flip()