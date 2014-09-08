#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"キーイベント")

img = pygame.image.load("python.png").convert_alpha()
img_rect = img.get_rect()
img_rect.center = (320, 240)

vx = vy = 10  # キーを押したときの移動距離

while True:
    screen.fill((0,0,255))
    screen.blit(img, img_rect)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == KEYDOWN:  # キーを押したとき
            # ESCキーならスクリプトを終了
            if event.key == K_ESCAPE:
                sys.exit()
            # 矢印キーなら画像を移動
            if event.key == K_LEFT:
                img_rect.move_ip(-vx, 0)
            if event.key == K_RIGHT:
                img_rect.move_ip(vx, 0)
            if event.key == K_UP:
                img_rect.move_ip(0, -vy)
            if event.key == K_DOWN:
                img_rect.move_ip(0, vy)
