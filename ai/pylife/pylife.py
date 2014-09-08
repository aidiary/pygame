#!/usr/bin/env python
#coding:utf-8
import pygame
from pygame.locals import *
import random
import sys

SCR_RECT = Rect(0, 0, 800, 600)  # スクリーンサイズ
CS = 10  # セルのサイズ
NUM_ROW = SCR_RECT.height / CS   # フィールドの行数
NUM_COL = SCR_RECT.width / CS  # フィールドの列数
DEAD, ALIVE = 0, 1  # セルの生死定数
RAND_LIFE = 0.1

class LifeGame:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Conway's Game of Life")
        self.font = pygame.font.SysFont(None, 16)
        # NUM_ROW x NUM_COLサイズのフィールド（2次元リスト）
        self.field = [[DEAD for x in range(NUM_COL)] for y in range(NUM_ROW)]
        self.generation = 0  # 世代数
        self.run = False  # シミュレーション実行中か？
        self.cursor = [NUM_COL/2, NUM_ROW/2]  # カーソルの位置
        # ライフゲームを初期化
        self.clear()
        # メインループ
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    # 矢印キーでカーソルを移動
                    elif event.key == K_LEFT:
                        self.cursor[0] -= 1
                        if self.cursor[0] < 0: self.cursor[0] = 0
                    elif event.key == K_RIGHT:
                        self.cursor[0] += 1
                        if self.cursor[0] > NUM_COL-1: self.cursor[0] = NUM_COL-1
                    elif event.key == K_UP:
                        self.cursor[1] -= 1
                        if self.cursor[1] < 0: self.cursor[1] = 0
                    elif event.key == K_DOWN:
                        self.cursor[1] += 1
                        if self.cursor[1] > NUM_ROW-1: self.cursor[1] = NUM_ROW-1
                    # スペースキーでカーソルのセルを反転
                    elif event.key == K_SPACE:
                        x, y = self.cursor
                        if self.field[y][x] == DEAD:
                            self.field[y][x] = ALIVE
                        elif self.field[y][x] == ALIVE:
                            self.field[y][x] = DEAD
                    # sキーでシミュレーション開始
                    elif event.key == K_s:
                            self.run = not self.run
                    # nキーで1世代だけ進める
                    elif event.key == K_n:
                        self.step()
                    # cキーでクリア
                    elif event.key == K_c:
                        self.clear()
                    # rキーでランダムに生きているセルを追加
                    elif event.key == K_r:
                        self.rand()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # 左ボタンクリックでセルを反転
                    px, py = event.pos
                    x, y = px/CS, py/CS
                    self.cursor = [x, y]
                    if self.field[y][x] == DEAD:
                        self.field[y][x] = ALIVE
                    elif self.field[y][x] == ALIVE:
                        self.field[y][x] = DEAD
    def clear(self):
        """ゲームを初期化"""
        self.generation = 0
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                self.field[y][x] = DEAD
    def rand(self):
        """ランダムに生きているセルを追加"""
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if random.random() < RAND_LIFE:
                    self.field[y][x] = ALIVE
    def update(self):
        """フィールドを更新"""
        if self.run:
            self.step()  # 1世代進める
    def step(self):
        """1世代だけ進める"""
        # 次のフィールド
        next_field = [[False for x in range(NUM_COL)] for y in range(NUM_ROW)]
        # ライフゲームの規則にしたがって次のフィールドをセット
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                num_alive_cells = self.around(x, y)
                if num_alive_cells == 2:
                    # 周囲の2セルが生きていれば維持
                    next_field[y][x] = self.field[y][x]
                elif num_alive_cells == 3:
                    # 周囲の3セルが生きていれば誕生
                    next_field[y][x] = ALIVE
                else:
                    # それ以外では死亡
                    next_field[y][x] = DEAD
        self.field = next_field
        self.generation += 1
    def draw(self, screen):
        """フィールドを描画"""
        # セルを描画
        for y in range(NUM_ROW):
            for x in range(NUM_COL):
                if self.field[y][x] == ALIVE:
                    pygame.draw.rect(screen, (255,255,0), Rect(x*CS,y*CS,CS,CS))
                elif self.field[y][x] == DEAD:
                    pygame.draw.rect(screen, (0,0,0), Rect(x*CS,y*CS,CS,CS))
                pygame.draw.rect(screen, (50,50,50), Rect(x*CS,y*CS,CS,CS), 1)  # グリッド
        # 中心線を描く
        pygame.draw.line(screen, (255,0,0), (0,SCR_RECT.height/2), (SCR_RECT.width,SCR_RECT.height/2))
        pygame.draw.line(screen, (255,0,0), (SCR_RECT.width/2,0), (SCR_RECT.width/2,SCR_RECT.height))
        # カーソルを描画
        pygame.draw.rect(screen, (0,0,255), Rect(self.cursor[0]*CS,self.cursor[1]*CS,CS,CS), 1)
        # ゲーム情報を描画
        screen.blit(self.font.render("generation:%d" % self.generation, True, (0,255,0)), (0,0))
        screen.blit(self.font.render("space : birth/kill", True, (0,255,0)), (0,12))
        screen.blit(self.font.render("s : start/stop", True, (0,255,0)), (0,24))
        screen.blit(self.font.render("n : next", True, (0,255,0)), (0,36))
        screen.blit(self.font.render("r : random", True, (0,255,0)), (0,48))
    def around(self, x, y):
        """(x,y)の周囲8マスの生きているセルの数を返す"""
        if x == 0 or x == NUM_COL-1 or y == 0 or y == NUM_ROW-1:
            return 0
        sum = 0
        sum += self.field[y-1][x-1]  # 左上
        sum += self.field[y-1][x]    # 上
        sum += self.field[y-1][x+1]  # 右上
        sum += self.field[y][x-1]    # 左
        sum += self.field[y][x+1]    # 右
        sum += self.field[y+1][x-1]  # 左下
        sum += self.field[y+1][x]    # 下
        sum += self.field[y+1][x+1]  # 右下
        return sum

if __name__ == "__main__":
    LifeGame()
