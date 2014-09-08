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
        pygame.display.set_caption("二段ジャンプ")
        
        # 画像のロード
        Python.left_image = load_image("python.png", -1)                     # 左向き
        Python.right_image = pygame.transform.flip(Python.left_image, 1, 0)  # 右向き
        Block.image = load_image("block.png", -1)
        
        # スプライトグループの作成
        self.all = pygame.sprite.RenderUpdates()
        self.blocks = pygame.sprite.Group()
        Python.containers = self.all
        Block.containers = self.all, self.blocks
        
        # パイソンの作成
        # 衝突判定用にブロックグループを渡す
        Python((300,200), self.blocks)
        
        # ブロックの作成
        self.create_blocks()

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
    
    def create_blocks(self):
        """ブロックの作成"""
        # 天井と床
        for x in range(20):
            Block((x*32, 0))
            Block((x*32, 14*32))
        
        # 左右の壁
        for y in range(20):
            Block((0, y*32))
            Block((19*32, y*32))
        
        # 中央のトンネル
        Block((192,384)); Block((224,384)); Block((256,384))
        Block((288,384)); Block((320,384)); Block((352,384))
        
        # 右下にある山
        Block((480,416)); Block((512,416)); Block((544,416)); Block((576,416))
        Block((512,384)); Block((544,384)); Block((576,384))
        Block((544,352)); Block((576,352))
        Block((576,320))
        
        # 左下から右上への階段
        Block((32,384));  Block((128,320)); Block((224,256)); Block((384,192))
        Block((416,192)); Block((448,192)); Block((480,192))
        Block((512,192)); Block((544,192)); Block((576,192))
        
        # 左上のブロック
        Block((128, 128))
        
class Python(pygame.sprite.Sprite):
    """パイソン"""
    MOVE_SPEED = 2.5    # 移動速度
    JUMP_SPEED = 6.0    # ジャンプの初速度
    GRAVITY = 0.2       # 重力加速度
    MAX_JUMP_COUNT = 2  # ジャンプ段数の回数
    
    def __init__(self, pos, blocks):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]  # 座標設定
        self.blocks = blocks  # 衝突判定用
        
        # ジャンプ回数
        self.jump_count = 0
        
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
        if pressed_keys[K_SPACE]:
            if self.on_floor:
                self.fpvy = - self.JUMP_SPEED  # 上向きに初速度を与える
                self.on_floor = False
                self.jump_count = 1
            elif not self.prev_button and self.jump_count < self.MAX_JUMP_COUNT:
                self.fpvy = -self.JUMP_SPEED
                self.jump_count += 1
            
        # 速度を更新
        if not self.on_floor:
            self.fpvy += self.GRAVITY  # 下向きに重力をかける
        
        self.collision_x()  # X方向の衝突判定処理
        self.collision_y()  # Y方向の衝突判定処理
        
        # 浮動小数点の位置を整数座標に戻す
        # スプライトを動かすにはself.rectの更新が必要！
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)
        
        # ボタンのジャンプキーの状態を記録
        self.prev_button = pressed_keys[K_SPACE]
        
    def collision_x(self):
        """X方向の衝突判定処理"""
        # パイソンのサイズ
        width = self.rect.width
        height = self.rect.height
        
        # X方向の移動先の座標と矩形を求める
        newx = self.fpx + self.fpvx
        newrect = Rect(newx, self.fpy, width, height)
        
        # ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                if self.fpvx > 0:    # 右に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.fpx = block.rect.left - width
                    self.fpvx = 0
                elif self.fpvx < 0:  # 左に移動中に衝突
                    self.fpx = block.rect.right
                    self.fpvx = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.fpx = newx
    
    def collision_y(self):
        """Y方向の衝突判定処理"""
        # パイソンのサイズ
        width = self.rect.width
        height = self.rect.height
        
        # Y方向の移動先の座標と矩形を求める
        newy = self.fpy + self.fpvy
        newrect = Rect(self.fpx, newy, width, height)
        
        # ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                if self.fpvy > 0:    # 下に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.fpy = block.rect.top - height
                    self.fpvy = 0
                    # 下に移動中に衝突したなら床の上にいる
                    self.on_floor = True
                    self.jump_count = 0  # ジャンプカウントをリセット
                elif self.fpvy < 0:  # 上に移動中に衝突
                    self.fpy = block.rect.bottom
                    self.fpvy = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.fpy = newy
                # 衝突ブロックがないなら床の上にいない
                self.on_floor = False

class Block(pygame.sprite.Sprite):
    """ブロック"""
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

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
