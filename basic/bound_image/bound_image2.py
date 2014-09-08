#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCR_WIDTH,SCR_HEIGHT = 640,480

pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
pygame.display.set_caption(u"画像の移動と跳ね返り処理2")

img = pygame.image.load("python.png").convert_alpha()
img_rect = img.get_rect()

vx = vy = 120  # 1秒間の移動ピクセル
clock = pygame.time.Clock()

while True:
    time_passed = clock.tick(60)  # 60fpsで前回からの経過時間を返す（ミリ秒）
    time_passed_seconds = time_passed / 1000.0  # ミリ秒を秒に変換

    # 画像の移動
    img_rect.x += vx * time_passed_seconds
    img_rect.y += vy * time_passed_seconds
    # 跳ね返り処理
    if img_rect.left < 0 or img_rect.right > SCR_WIDTH:
        vx = -vx
    if img_rect.top < 0 or img_rect.bottom > SCR_HEIGHT:
        vy = -vy
    
    screen.fill((0,0,255))
    screen.blit(img, img_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE: sys.exit()
