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
    pygame.display.set_caption(u"PyMap 03 マップチップパレット")
    
    # マップチップをロード
    load_mapchips("mapchip.dat")
    
    palette = MapchipPalette()
    map = Map("new.map", 64, 64, palette)
    cursor = Cursor(0, 0)
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        if palette.display_flag:  # パレットが表示中なら
            palette.update()
            palette.draw(screen)
        else:
            offset = calc_offset(cursor)
            # 更新
            cursor.update()
            map.update(offset)
            # 描画
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
            elif event.type == KEYDOWN and event.key == K_SPACE:
                # パレットの表示/非表示を切り替え
                palette.display_flag = not palette.display_flag

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
    def __init__(self, name, row, col, palette):
        self.name = name
        self.row = row
        self.col = col
        self.default = 5  # デフォルトのマップチップ番号
        self.map = [[self.default for c in range(self.col)] for r in range(self.row)]
        self.palette = palette
    def __str__(self):
        return "%s,%d,%d,%d" % (self.name, self.row, self.col, self.default)
    def update(self, offset):
        offsetx, offsety = offset
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # 左クリック（マップチップ描画）
            # マウスが返すのはローカル座標
            px, py = pygame.mouse.get_pos()
            # 全体マップ上での座標はoffsetを足せばよい
            # GSで割るのはピクセルをマスに直すため
            selectx = (px + offsetx) / GS
            selecty = (py + offsety) / GS
            # マップ範囲外だったら無視
            if selectx < 0 or selecty < 0 or selectx > self.col-1 or selecty > self.row-1:
                 return
            # パレットで選択中のマップチップでマップを更新
            self.map[selecty][selectx] = self.palette.selected_mapchip
        elif mouse_pressed[2]:  # 右クリック（マップチップ抽出）
            px, py = pygame.mouse.get_pos()
            selectx = (px + offsetx) / GS
            selecty = (py + offsety) / GS
            if selectx < 0 or selecty < 0 or selectx > self.col-1 or selecty > self.row-1:
                 return
            self.palette.selected_mapchip = self.map[selecty][selectx]
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

class MapchipPalette:
    """マップチップパレット"""
    ROW = 20  # パレットの行数
    COL = 25  # パレットの列数
    COLOR = (0,255,0)  # 緑
    WIDTH = 3  # カーソルの太さ
    def __init__(self):
        self.display_flag = False  # Trueのときパレット表示
        self.selected_mapchip = 3  # 選択しているマップチップ番号
    def update(self):
        # マップチップパレットの選択
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # 左クリック
            # マウス座標を取得
            mouse_pos = pygame.mouse.get_pos()
            # マス座標に変換
            x = mouse_pos[0] / GS
            y = mouse_pos[1] / GS
            # マップチップ番号に変換
            n = y * self.COL + x
            if n < len(Map.images) and Map.images[n] != None:
                self.selected_mapchip = n
                self.display_flag = False  # パレットを消す
                # パレットが消えた直後にマップチップを描画してしまうのを防ぐ
                pygame.time.wait(500)
    def draw(self, screen):
        # パレットを描画
        for i in range(self.ROW * self.COL):
            x = (i % self.COL) * GS
            y = (i / self.COL) * GS
            image = Map.images[0]
            try:
                if Map.images[i] != None:
                    image = Map.images[i]
            except IndexError:  # イメージが登録されてないとき
                image = Map.images[0]
            screen.blit(image, (x,y))
        # マウスの位置にカーソルを描画
        mouse_pos = pygame.mouse.get_pos()
        x = mouse_pos[0] / GS
        y = mouse_pos[1] / GS
        pygame.draw.rect(screen, self.COLOR, (x*GS,y*GS,GS,GS), self.WIDTH)

def load_image(filename, colorkey=None):
    filename = os.path.join("mapchip", filename)
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

def load_mapchips(file):
    """マップチップをロードしてMap.imagesに格納"""
    fp = open(file, "r")
    for line in fp:
        line = line.rstrip()  # 改行除去
        data = line.split(",")  # カンマで分解
        id = int(data[0])  # マップチップID
        name = data[1]  # マップチップ名
        movable = int(data[2])  # 移動可能か？（エディタでは未使用）
        Map.images.append(load_image("%s.png" % name))
    fp.close()

if __name__ == "__main__":
    main()
