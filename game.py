from array import array
from curses import echo
import os
from queue import Empty
import struct
import pygame as pg
import math
from bs4 import BeautifulSoup

size = width, height = 843, 480
white = 255, 255, 255

def ccw(A,B,C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersect(A, B):
        return ccw(A[0], B[0], B[1]) != ccw(A[1], B[0], B[1]) and ccw(A[0], A[1], B[0]) != ccw(A[0], A[1], B[1])

pg.init()
window = pg.display.set_mode(size)
scene = pg.image.load(os.path.join('test.png'))
scene.convert_alpha()
pg.display.flip() 




clock = pg.time.Clock()

with open('test.svg', 'r') as f:
	data = f.read()
Bs_data = BeautifulSoup(data, "xml")


with open('test2.svg', 'r') as f2:
	data2 = f2.read()
Bs_data2 = BeautifulSoup(data2, "xml")

collisionFloor = []
collisionWall = []
collisionCeiling = []

def lolinit():
	del collisionFloor[:]
	del collisionWall[:]
	del collisionCeiling[:]
	for each in b_unique:
		tmp = (float(each.get('x')), float(each.get('y')), float(each.get('x'))+float(each.get('width')), float(each.get('y'))+float(each.get('height')))
		collisionFloor.append(((tmp[0], tmp[1]), (tmp[2], tmp[1])))
		collisionWall.append(((tmp[2], tmp[1]), (tmp[2], tmp[3])))
		collisionCeiling.append(((tmp[0], tmp[3]), (tmp[2], tmp[3])))
		collisionWall.append(((tmp[0], tmp[1]), (tmp[0], tmp[3])))

b_unique = Bs_data.find_all('rect')
lolinit()

plPos = [50, 300]
plSpd = [0, 0]
plSize = (20, 20)

floorTouch = False



while True:
	clock.tick(60)
	window.fill(white)
	window.blit(scene, (0, 0))
	#if not floorTouch:
	plSpd[1] -= 0.2
	
	frameTrace = ((plPos[0], plPos[1]), (plPos[0]-plSpd[0], plPos[1]-plSpd[1]))


	floorTouch = False
	for each in collisionFloor:
		if intersect(each, frameTrace):
			floorTouch = True
			if plSpd[1] < 0:
				plSpd[1] = 0

	for each in collisionWall:
		if intersect(each, frameTrace):
			wallTouch = True
			plSpd[0] *= -0.5
	
	for each in collisionCeiling:
		if intersect(each, frameTrace):
			if plSpd[1] > 0:
				plSpd[1] = 0


	# for each in b_unique:
	# 	pg.draw.rect(window, (0, 0, 0), pg.Rect(
	# 		float(each.get('x')), 
	# 		float(each.get('y')), 
	# 		float(each.get('width')), 
	# 		float(each.get('height'))))


	pg.draw.rect(window, (0, 0, 255), pg.Rect((plPos[0]-plSize[0]/2, plPos[1]-plSize[1]/2), plSize))
 


	pg.display.flip()
	for event in pg.event.get():
		if event.type == pg.QUIT: raise SystemExit
		if event.type == pg.KEYDOWN:
			if pg.key.get_pressed()[pg.K_SPACE] and floorTouch:
				floorTouch = False
				plSpd[1] = 10
			if pg.key.get_pressed()[pg.K_w]:
				b_unique = []
				b_unique = Bs_data2.find_all('rect')
				lolinit()
				scene = pg.image.load(os.path.join('test2.png'))
				scene.convert_alpha()
			if pg.key.get_pressed()[pg.K_s]:
				b_unique = []
				b_unique = Bs_data.find_all('rect')
				lolinit()
				scene = pg.image.load(os.path.join('test.png'))
				scene.convert_alpha()



	if floorTouch:
		if pg.key.get_pressed()[pg.K_a]:
			plSpd[0] = 3
		elif pg.key.get_pressed()[pg.K_d]:
			plSpd[0] = -3
		else:
			plSpd[0] = 0



	plPos[0] -= plSpd[0]
	plPos[1] -= plSpd[1]
	plPos[0] %= width
	plPos[1] %= height