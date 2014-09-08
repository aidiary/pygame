#!/usr/bin/env python
#coding:utf-8
import pygame
from pygame.locals import *
import os
import sys

SCR_RECT = Rect(0, 0, 800, 640)
GS = 32

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"PyMap 01 カーソルの移動")
    
    # イメージをロード
    Map.images.append(load_image("none.png"))   # 範囲外
    Map.images.append(load_image("water.png"))  # 海
    
    map = Map("new.map", 64, 64)  # 64x64（単位：マス）のマップ
    cursor = Cursor(0, 0)
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        offset = calc_offset(cursor)
        cursor.update()
        map.draw(screen, offset)
        cursor.draw(screen, offset)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

class Cursor:
    COLOR = (0,255,0)  # 緑色
    WIDTH = 3  # 太さ
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = Rect(x*GS, y*GS, GS, GS)
    def update(self):
        # キー入力でカーソルを移動
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_DOWN]:
            self.y += 1
        elif pressed_keys[K_LEFT]:
            self.x -= 1
        elif pressed_keys[K_RIGHT]:
            self.x += 1
        elif pressed_keys[K_UP]:
            self.y -= 1
        self.rect = Rect(self.x*GS, self.y*GS, GS, GS)
    def draw(self, screen, offset):
        # オフセットを考慮してカーソルを描画
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        pygame.draw.rect(screen, self.COLOR, (px-offsetx,py-offsety,GS,GS), self.WIDTH)

class Map:
    images = []
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col
        self.default = 1  # デフォルトのマップチップ番号
        # デフォルトマップチップで初期化
        self.map = [[self.default for c in range(self.col)] for r in range(self.row)]
    def __str__(self):
        return "%s,%d,%d,%d" % (self.name, self.row, self.col, self.default)
    def draw(self, screen, offset):
        offsetx, offsety = offset
        # マップの描画範囲を計算
        startx = offsetx / GS
        endx = startx + SCR_RECT.width/GS + 2
        starty = offsety / GS
        endy = starty + SCR_RECT.height/GS + 2
        # マップの描画
        for y in range(starty, endy):
            for x in range(startx, endx):
                # マップの範囲外はマップチップ番号0で描画
                if x < 0 or y < 0 or x > self.col-1 or y > self.row-1:
                    screen.blit(self.images[0], (x*GS-offsetx,y*GS-offsety))
                else:
                    screen.blit(self.images[self.map[y][x]], (x*GS-offsetx,y*GS-offsety))

def load_image(filename, colorkey=None):
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
    return image

def calc_offset(cursor):
    """cursorを中心としてオフセットを計算する"""
    offsetx = cursor.rect.topleft[0] - SCR_RECT.width/2
    offsety = cursor.rect.topleft[1] - SCR_RECT.height/2
    return offsetx, offsety

if __name__ == "__main__":
    main()
