#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import os
import sys

SCR_RECT = Rect(0, 0, 372, 384)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"Breakout 01 パドルを動かす")
    
    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    Paddle.containers = all
    # パドルを作成
    paddle = Paddle()
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        all.update()
        all.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

class Paddle(pygame.sprite.Sprite):
    """ボールを打つパドル"""
    def __init__(self):
        # containersはmain()でセットされる
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image("paddle.png")
        self.rect.bottom = SCR_RECT.bottom  # パドルは画面の一番下
    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]  # パドルの中央のX座標=マウスのX座標
        self.rect.clamp_ip(SCR_RECT)  # SCR_RECT内でしか移動できなくなる

def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

if __name__ == "__main__":
    main()
