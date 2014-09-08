#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"イメージの描画")

# イメージを用意
backImg = pygame.image.load("moriyama.jpg").convert()     # 背景
pythonImg = pygame.image.load("python.png").convert_alpha()  # 蛇

while True:
    screen.blit(backImg, (0,0))        # 背景を描画
    screen.blit(pythonImg, (320,400))  # 蛇を描画
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
