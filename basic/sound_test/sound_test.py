#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCR_WIDTH,SCR_HEIGHT = 640,480

pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
pygame.display.set_caption(u"サウンドテスト")

# 画像をロード
img = pygame.image.load("python.png").convert_alpha()
img_rect = img.get_rect()

# サウンドをロード
hit_sound = pygame.mixer.Sound("hit.wav")

vx = vy = 300  # 1秒間の移動ピクセル
clock = pygame.time.Clock()

# BGMを再生
pygame.mixer.music.load("tam-n11.mp3")
pygame.mixer.music.play(-1)

while True:
    time_passed = clock.tick(60)
    time_passed_seconds = time_passed / 1000.0

    # 画像の移動
    img_rect.x += vx * time_passed_seconds
    img_rect.y += vy * time_passed_seconds
    
    # 壁にぶつかると跳ね返る
    if img_rect.left < 0 or img_rect.right > SCR_WIDTH:
        hit_sound.play()  # サウンドを再生
        vx = -vx
    if img_rect.top < 0 or img_rect.bottom > SCR_HEIGHT:
        hit_sound.play()  # サウンドを再生
        vy = -vy
    
    screen.fill((0,0,255))
    screen.blit(img, img_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE: sys.exit()
