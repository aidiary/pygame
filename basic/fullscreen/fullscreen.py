#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCR_RECT = Rect(0, 0, 640, 480)

class MySprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self, self.containers)  # デフォルトグループをセット
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        # 壁にぶつかったら跳ね返る
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
            self.vy = -self.vy
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"フルスクリーンモード")
    # スプライトグループを作成してスプライトクラスに割り当て
    group = pygame.sprite.RenderUpdates()
    MySprite.containers = group
    # スプライトを作成
    python1 = MySprite("python.png", 0, 0, 2, 2)
    python2 = MySprite("python.png", 10, 10, 5, 5)
    python3 = MySprite("python.png", 320, 240, -2, 3)
    clock = pygame.time.Clock()
    fullscreen_flag = False
    while True:
        clock.tick(60)  # 60fps
        screen.fill((0,0,255))
        # スプライトグループを更新
        group.update()
        # スプライトグループを描画
        group.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_F2:
                # F2キーでフルスクリーンモードへの切り替え
                fullscreen_flag = not fullscreen_flag
                if fullscreen_flag:
                    screen = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode(SCR_RECT.size, 0, 32)

if __name__ == "__main__":
    main()
