from sys import exit
import pygame
import math
from pygame.locals import *

screenx = 640
screeny = 480
framerate = 60
black = 0,0,0
white = 255,255,255
degs = math.pi / 180
debug = False
scale = 1              #graphics scale factor (must be integer)

stop_limit = 0.005  #when speed is less than this, ship stops
drag = 0.01      #should be less than 1!!!
accel = 0.07
turn = 0.3
debounce = 10
damper = False

bounce = 0
heading = 0
theta = 0
toturn = 0
reverse = 0

pygame.init()
screen = pygame.display.set_mode((screenx,screeny))
clock = pygame.time.Clock()

panel = pygame.image.load('panel.gif')
panel = pygame.transform.scale(panel,(320*scale,40*scale))
red = pygame.image.load('red.gif')
red = pygame.transform.scale(red,(7*scale,7*scale))
grn = pygame.image.load('grn.gif')
grn = pygame.transform.scale(grn,(7*scale,7*scale))

class Player(object):
	def __init__(self):
		self.sx = screenx/2
		self.sy = screeny/2
		self.vx = 0
		self.vy = 0
		self.angle = -90

player = Player()

pygame.key.set_repeat(1,1)

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	
	#correct player.angle so that it is between -pi and +pi
	if player.angle > 180: player.angle -= 360
	if player.angle < -180: player.angle += 360
	
	#calculate the player's true heading (the actual direction of travel)
	if player.vx == 0:
		if player.vy > 0:
			heading = (math.pi/2)
		elif player.vy < 0:
			heading = (-math.pi/2)
		if player.vy == 0:
			heading = 0
	else:
		if player.vx < 0 and player.vy > 0:
			heading = math.atan(abs(player.vx)/abs(player.vy)) + (math.pi/2)
		elif player.vx > 0 and player.vy < 0:
			heading = -math.atan(abs(player.vy)/abs(player.vx))
		elif player.vx < 0 and player.vy < 0:
			heading = -math.atan(abs(player.vx)/abs(player.vy)) - (math.pi/2)
		elif player.vx > 0 and player.vy > 0:
			heading = math.atan(abs(player.vy)/abs(player.vx))
		elif player.vx == 0 and not player.vy == 0:
			if player.vy > 0: heading = math.pi/2
			else: heading = -math.pi/2
		elif player.vy == 0 and not player.vx == 0:
			if player.vx > 0: heading = 0
			else: heading = math.pi
		else: pass
	
	#toturn = how far the ship must turn to face the opposite of its true heading
	if heading == 0:
		reverse = math.pi
	elif heading > 0:
		reverse = heading - math.pi
	elif heading < 0:
		reverse = heading + math.pi
	toturn = reverse - (player.angle*degs)
	if toturn < -math.pi:
		toturn += 2*math.pi
	if toturn == -math.pi:
		toturn = math.pi
	
	#get keyboard input and act accordingly
	keys = pygame.key.get_pressed()
	
	if keys[K_LEFT]: #turn right
		player.angle -= 10 * turn
		
	if keys[K_RIGHT]: #turn left
		player.angle += 10 * turn
		
	if keys[K_DOWN]: #turn so that true heading is astern
		if player.vx == 0 and player.vy == 0:
			pass #do nothing if stationary
		elif abs(toturn) > 10*turn*degs:
			if toturn > 0:
				player.angle += 10*turn
			else:
				player.angle -= 10*turn
		else:
			player.angle += (toturn/degs)

	if keys[K_UP]: #thrust!
		player.vx += (math.cos((player.angle)*degs)) * accel
		player.vy += (math.sin((player.angle)*degs)) * accel
		
	if keys[K_SPACE] and bounce == 0: #toggle inertial dampers
		damper = not(damper)
		bounce = debounce
		if debug:
			if damper:
				print "Inertial dampers ON"
			else:
				print "Intertial dampers OFF"
			
	#count-down de-bounce timer to 0
	if bounce > 0: bounce -= 1
	
	#debug output
	if debug:
		print "\nHeading: " + str(heading)
		print "Angle:   " + str(player.angle*degs)
		print "To Turn: " + str(toturn)
		print "reverse: " + str(reverse)
	
	#calculate position of three triangle points to draw the ship
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
	
	#when ship's speed is almost zero, make it zero
	if (player.vx < stop_limit) and (player.vx > (- stop_limit)): player.vx = 0
	if (player.vy < stop_limit) and (player.vy > (- stop_limit)): player.vy = 0
	
	#decelerate due to drag when inertial dampers are on
	if damper:
		player.vx -= player.vx * drag
		player.vy -= player.vy * drag
	
	#move the ship by velocity
	player.sx += player.vx
	player.sy += player.vy
	
	#wrap-around when flying off-screen
	if player.sx > screenx: player.sx = 0
	if player.sy > screeny: player.sy = 0
	if player.sx < 0: player.sx = screenx
	if player.sy < 0: player.sy = screeny
	
	#draw graphics
	screen.fill(black)
	pygame.draw.polygon(screen, white, points, 2)
	panel_y = screeny-(40*scale)
	screen.blit(panel,(0,panel_y))
	if damper:
		screen.blit(grn,(54*scale,(panel_y+22*scale)))
	else:
		screen.blit(red,(54*scale,(panel_y+22*scale)))
	
	#limit frame rate
	clock.tick(framerate)
	
	#flip/refresh screen
	pygame.display.flip()