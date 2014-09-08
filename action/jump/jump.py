#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import os
import sys

SCR_RECT = Rect(0, 0, 640, 480)

class PyAction:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("ジャンプ")
        
        # 画像のロード
        Python.left_image = load_image("python.png", -1)                     # 左向き
        Python.right_image = pygame.transform.flip(Python.left_image, 1, 0)  # 右向き
        
        # オブジェクとグループと蛇の作成
        self.all = pygame.sprite.RenderUpdates()
        Python.containers = self.all
        Python()
        
        # メインループ
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def update(self):
        """スプライトの更新"""
        self.all.update()
    
    def draw(self, screen):
        """スプライトの描画"""
        screen.fill((0,0,0))
        self.all.draw(screen)
    
    def key_handler(self):
        """キー入力処理"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

class Python(pygame.sprite.Sprite):
    """パイソン"""
    MOVE_SPEED = 5.0  # 移動速度
    JUMP_SPEED = 8.0  # ジャンプの初速度
    GRAVITY = 0.2     # 重力加速度
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom
        
        # 浮動小数点の位置と速度
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0.0
        self.fpvy = 0.0
        
        # 地面にいるか？
        self.on_floor = False
        
    def update(self):
        """スプライトの更新"""
        # キー入力取得
        pressed_keys = pygame.key.get_pressed()

        # 左右移動
        if pressed_keys[K_RIGHT]:
            self.image = self.right_image
            self.fpvx = self.MOVE_SPEED
        elif pressed_keys[K_LEFT]:
            self.image = self.left_image
            self.fpvx = -self.MOVE_SPEED
        else:
            self.fpvx = 0.0
        
        # ジャンプ
        if pressed_keys[K_UP]:
            if self.on_floor:
                self.fpvy = - self.JUMP_SPEED  # 上向きに初速度を与える
                self.on_floor = False
        
        # 速度を更新
        if not self.on_floor:
            self.fpvy += self.GRAVITY  # 下向きに重力をかける
        
        # 浮動小数点の位置を更新
        self.fpx += self.fpvx
        self.fpy += self.fpvy
        
        # 着地したか調べる
        if self.fpy > SCR_RECT.height - self.rect.height:
            self.fpy = SCR_RECT.height - self.rect.height  # 床にめり込まないように位置調整
            self.fpvy = 0
            self.on_floor = True
        
        # 浮動小数点の位置を整数座標に戻す
        # スプライトを動かすにはself.rectの更新が必要！
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

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
    return image

if __name__ == "__main__":
    PyAction()
