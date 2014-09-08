#!/usr/bin/env python
#coding:utf-8
import pygame
from pygame.locals import *
import math
import sys

SCR_RECT = Rect(0, 0, 640, 480)
START = (320, 240)  # ファイアボールの始点

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"ファイアボール")
    
    # スプライトグループ
    all = pygame.sprite.RenderUpdates()
    Fireball.containers = all
    # スプライトの画像を登録
    Fireball.image = load_image("fireball.png")
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        mouse_handler()
        all.update()
        all.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

def mouse_handler():
    """マウスイベントを検知してファイアボールを発射"""
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        x, y = pygame.mouse.get_pos()
        Fireball(START, (x,y))

class Fireball(pygame.sprite.Sprite):
    """ファイアボール"""
    speed = 10
    def __init__(self, start, target):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        # 始点と終点をセット
        self.start = start
        self.target = target
        self.rect.center = self.start
        # 終点の角度を計算
        self.direction = math.atan2(target[1]-start[1], target[0]-start[0])
        # 速度を計算
        self.vx = math.cos(self.direction) * self.speed
        self.vy = math.sin(self.direction) * self.speed
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        # 画面外に出たらオブジェクトを破棄
        if not SCR_RECT.contains(self.rect):
            self.kill()

def load_image(filename, colorkey=None):
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
    return image

if __name__ == "__main__":
    main()
