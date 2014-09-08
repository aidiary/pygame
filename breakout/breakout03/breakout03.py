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
    pygame.display.set_caption(u"Breakout 03 ブロックを壊す")
    
    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()  # 描画用グループ
    bricks = pygame.sprite.Group()       # 衝突判定用グループ
    Paddle.containers = all
    Ball.containers = all
    Brick.containers = all, bricks
    
    # パドル
    paddle = Paddle()
    # ブロックを作成
    # 自動的にbricksグループに追加される
    for x in range(1, 11):  # 1列から10列まで
        for y in range(1, 6):  # 1行から5行まで
            Brick(x, y)
    # ボールを作成
    Ball(paddle, bricks)
    
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

class Ball(pygame.sprite.Sprite):
    """ボール"""
    speed = 5
    def __init__(self, paddle, bricks):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image("ball.png")
        self.dx = self.dy = 0  # ボールの速度
        self.paddle = paddle  # パドルへの参照
        self.bricks = bricks  # ブロックグループへの参照
        self.update = self.start
    def start(self):
        """ボールの位置を初期化"""
        # パドルの中央に配置
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        # 左クリックで移動開始
        if pygame.mouse.get_pressed()[0] == 1:
            self.dx = self.speed
            self.dy = -self.speed
            # update()をmove()に置き換え
            self.update = self.move
    def move(self):
        """ボールの移動"""
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        # 壁との反射
        if self.rect.left < SCR_RECT.left:  # 左側
            self.rect.left = SCR_RECT.left
            self.dx = -self.dx  # 速度を反転
        if self.rect.right > SCR_RECT.right:  # 右側
            self.rect.right = SCR_RECT.right
            self.dx = -self.dx
        if self.rect.top < SCR_RECT.top:  # 上側
            self.rect.top = SCR_RECT.top
            self.dy = -self.dy
        # パドルとの反射
        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            self.dy = -self.dy
        # ボールを落とした場合
        if self.rect.top > SCR_RECT.bottom:
            self.update = self.start  # ボールを初期状態に
        # ブロックを壊す
        # ボールと衝突したブロックリストを取得
        bricks_collided = pygame.sprite.spritecollide(self, self.bricks, True)
        if bricks_collided:  # 衝突ブロックがある場合
            oldrect = self.rect
            for brick in bricks_collided:  # 各衝突ブロックに対して
                # ボールが左から衝突
                if oldrect.left < brick.rect.left < oldrect.right < brick.rect.right:
                    self.rect.right = brick.rect.left
                    self.dx = -self.dx
                # ボールが右から衝突
                if brick.rect.left < oldrect.left < brick.rect.right < oldrect.right:
                    self.rect.left = brick.rect.right
                    self.dx = -self.dx
                # ボールが上から衝突
                if oldrect.top < brick.rect.top < oldrect.bottom < brick.rect.bottom:
                    self.rect.bottom = brick.rect.top
                    self.dy = -self.dy
                # ボールが下から衝突
                if brick.rect.top < oldrect.top < brick.rect.bottom < oldrect.bottom:
                    self.rect.top = brick.rect.bottom
                    self.dy = -self.dy

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image("brick.png")
        # ブロックの位置を更新
        self.rect.left = SCR_RECT.left + x * self.rect.width
        self.rect.top = SCR_RECT.top + y * self.rect.height

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
