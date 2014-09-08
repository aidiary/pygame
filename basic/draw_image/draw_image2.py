#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"透明色の指定")

planeImg = pygame.image.load("plane.png").convert()

# 透明色を指定したイメージを作成
planeImg2 = pygame.image.load("plane.png").convert()
colorkey = planeImg2.get_at((0,0))  # 左上の色を透明色に
planeImg2.set_colorkey(colorkey, RLEACCEL)

while True:
    screen.fill((0,0,0))
    screen.blit(planeImg, (100,100))
    screen.blit(planeImg2, (200,100))
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
