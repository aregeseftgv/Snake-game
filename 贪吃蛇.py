# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:56:32 2021

@author: 13370
"""

import random
import pygame
import sys
import time
from pygame.locals import *   #导入所有pygame.locals里的变量
import Rect
import drawGamespeed

#创建一个游戏窗口 
DISPLAY = pygame.display.set_mode((600,400))
# 设置游戏窗口的标题
pygame.display.set_caption('贪吃蛇')
# 定义一个变量来控制游戏速度
FPSCLOCK = pygame.time.Clock()
#定义游戏界面需要使用的字体
BASICFONT = pygame.font.SysFont("arial",80)   #(name,size)  #一开始写了宋体，然后报错了......

# 定义颜色变量
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(255,0,0)
GREY = pygame.Color(150,150,150)

'''初始化贪吃蛇及食物'''
#贪吃蛇的初始位置
s_Head = [100,100]
# 初始化贪吃蛇的长度 (注：这里以20*20为一个标准小格子)
s_Body = [[80,100],[60,100],[40,100],[20,100]]
# 指定蛇初始前进的方向，向右
direction = "RIGHT"

# 设置第一个食物的位置
f_Position = [300,300]
# 对食物进行标记：0代表食物已被吃掉；1代表未被吃掉。
f_flag = 1

#绘制贪吃蛇、食物、分数等信息
# 绘制贪吃蛇
def drawSnake(s_Body):
    for i in s_Body:
        pygame.draw.rect(DISPLAY, WHITE, Rect(i[0], i[1], 20, 20))

# 绘制食物的位置
def drawFood(f_Position):
    pygame.draw.rect(DISPLAY, RED, Rect(f_Position[0], f_Position[1], 20, 20))

# 打印出当前得分
def drawScore(score):
    # 设置分数的显示颜色
    score_Surf = BASICFONT.render('%s' %(score), True, GREY)
    # 设置分数的位置,显示在屏幕右上角
    score_Rect = score_Surf.get_rect()
    score_Rect.midtop = (320, 240)
    
    # 绑定以上设置到句柄
    DISPLAY.blit(score_Surf, score_Rect)
    
#定义函数，用于展示游戏结束的画面并退出程序
# 游戏结束并退出  用def GameOver():    
def GameOver():
    # 设置GameOver的显示颜色
    GameOver_Surf = BASICFONT.render('Game Over!', True, GREY)
    # 设置GameOver的位置
    GameOver_Rect = GameOver_Surf.get_rect()
    GameOver_Rect.midtop = (320, 10)
    # 绑定以上设置到句柄
    DISPLAY.blit(GameOver_Surf, GameOver_Rect)

    pygame.display.flip()
    # 等待5秒
    time.sleep(5)
    # 退出游戏
    pygame.quit()
    # 退出程序
    sys.exit()

#设置一个游戏标志，以便于退出循环，初始为True
game_flag = True
while game_flag:
	# 渲染底色
	DISPLAY.fill(BLACK)
	# 画出贪吃蛇
	drawSnake(s_Body)
	# 画出食物位置
	drawFood(f_Position)
	# 打印出玩家的分数
	drawScore(len(s_Body) - 3)
	# 控制游戏速度, 根据贪吃蛇的蛇身长度来控制游戏速度
	# 玩家每吃三次，增加一次游戏速度，初始为2。可以根据需要调整。
	game_speed = 1 + len(s_Body) // 3
	# 打印出游戏速度
	drawGamespeed(game_speed)

	# 刷新pygame的显示层，贪吃蛇与食物的每一次移动，都会刷新显示层的操作来显示
	pygame.display.flip()
	# print (game_speed)
	FPSCLOCK.tick(game_speed)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# 接收到退出事件后，退出程序
			pygame.quit()
			sys.exit()

		# 判断键盘事件，用方向键或WASD来表示上下左右
		elif event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "DOWN":
				direction = "UP"
			if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "UP":
				direction = "DOWN"
			if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "RIGHT":
				direction = "LEFT"
			if (event.key == pygame.K_RIGHT or event.key == pygame.K_d)  and direction != "LEFT":
				direction = "RIGHT"
			# 点击空格退出游戏
			if (event.key == pygame.K_SPACE):
				game_flag = False
				GameOver()
                
	# 根据键盘的输入，改变蛇头方向，进行转弯
	if direction == "LEFT":
		s_Head[0] -= 20
	if direction == "RIGHT":
		s_Head[0] += 20
	if direction == "UP":
		s_Head[1] -= 20
	if direction == "DOWN":
		s_Head[1] += 20

	# 将蛇头当前位置加入到蛇身的列表中
	s_Body.insert(0, list(s_Head))
	"""如果蛇头与食物的位置重合，则判定吃到食物，将食物数量清零；
	   而没吃到食物的话，蛇身就会跟着蛇头运动"""
	# 判断蛇是否已经吃掉食物
	if s_Head[0] == f_Position[0] and s_Head[1] == f_Position[1]:
		f_flag = 0
	else:
		s_Body.pop()

	# 当游戏界面中的食物数量为0时， 需要重新生成食物，利用random函数来生成随机位置
	# 生成新的食物
	if f_flag == 0:
		# 随机生成x, y
		x = random.randrange(1, 32)
		y = random.randrange(1,24)
		f_Position = [int(x * 20), int(y * 20)]
		f_flag = 1

	# 判断游戏是否结束
	# 贪吃蛇触碰到边界
	if s_Head[0] < 0 or s_Head[0] > 640:
		GameOver()
	if s_Head[1] < 0 or s_Head[1] > 460:
		GameOver()

	# 贪吃蛇碰到自己
	for i in s_Body[1:]:
		if s_Head[0] == i[0] and s_Head[1] == i[1]:
			GameOver()