#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"フォントファイルのロード")

# フォントの作成
myfont = pygame.font.Font("ipag.ttf", 80)

# テキストを描画したSurfaceを作成
hello1 = myfont.render(u"こんにちは！", False, (0,0,0))
hello2 = myfont.render(u"こんにちは！", True, (0,0,0))
hello3 = myfont.render(u"こんにちは！", True, (255,0,0), (255,255,0))

while True:
    screen.fill((0,0,255))
    
    # テキストを描画する
    screen.blit(hello1, (20,50))
    screen.blit(hello2, (20,150))
    screen.blit(hello3, (20,250))
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
