#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import codecs
import os
import random
import sys

SCR_RECT = Rect(0, 0, 640, 480)
GS = 32
DOWN,LEFT,RIGHT,UP = 0,1,2,3
STOP, MOVE = 0, 1  # 移動タイプ
PROB_MOVE = 0.005  # 移動確率

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"PyRPG 13 メッセージウィンドウの表示")
    # キャラクターイメージをロード
    Character.images["player"] = split_image(load_image("player.png"))
    Character.images["king"] = split_image(load_image("king.png"))
    Character.images["minister"] = split_image(load_image("minister.png"))
    Character.images["soldier"] = split_image(load_image("soldier.png"))
    # マップチップをロード
    Map.images[0] = load_image("grass.png") # 草地
    Map.images[1] = load_image("water.png")  # 水
    Map.images[2] = load_image("forest.png") # 森
    Map.images[3] = load_image("hill.png")   # 丘
    Map.images[4] = load_image("mountain.png")  # 山
    # マップとプレイヤー作成
    map = Map("test2")
    player = Player("player", (1,1), DOWN)
    map.add_chara(player)
    # ウィンドウ
    wnd = Window(Rect(140,334,360,140))
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        # ウィンドウ表示中は更新を中止
        if not wnd.is_visible:
            map.update()
        offset = calc_offset(player)
        map.draw(screen, offset)
        wnd.draw(screen)  # ウィンドウの描画
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                if wnd.is_visible:  # ウィンドウ表示中
                    wnd.hide()  # ウィンドウを隠す
                else:
                    wnd.show()  # ウィンドウを表示

def calc_offset(player):
    """オフセットを計算する"""
    offsetx = player.rect.topleft[0] - SCR_RECT.width/2
    offsety = player.rect.topleft[1] - SCR_RECT.height/2
    return offsetx, offsety

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

def split_image(image):
    """128x128のキャラクターイメージを32x32の16枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    imageList = []
    for i in range(0, 128, GS):
        for j in range(0, 128, GS):
            surface = pygame.Surface((GS,GS))
            surface.blit(image, (0,0), (j,i,GS,GS))
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
            surface.convert()
            imageList.append(surface)
    return imageList

class Map:
    images = [None] * 256  # マップチップ（番号->イメージ）
    def __init__(self, name):
        self.name = name
        self.row = -1  # 行数
        self.col = -1  # 列数
        self.map = []  # マップデータ（2次元リスト）
        self.charas = []  # マップにいるキャラクターリスト
        self.load()  # マップをロード
        self.load_event()  # イベントをロード
    def add_chara(self, chara):
        """キャラクターをマップに追加する"""
        self.charas.append(chara)
    def update(self):
        """マップの更新"""
        # マップにいるキャラクターの更新
        for chara in self.charas:
            chara.update(self)  # mapを渡す
    def draw(self, screen, offset):
        """マップを描画する"""
        offsetx, offsety = offset
        # マップの描画範囲を計算
        startx = offsetx / GS
        endx = startx + SCR_RECT.width/GS + 1
        starty = offsety / GS
        endy = starty + SCR_RECT.height/GS + 1
        # マップの描画
        for y in range(starty, endy):
            for x in range(startx, endx):
                # マップの範囲外はデフォルトイメージで描画
                # この条件がないとマップの端に行くとエラー発生
                if x < 0 or y < 0 or x > self.col-1 or y > self.row-1:
                    screen.blit(self.images[self.default], (x*GS-offsetx,y*GS-offsety))
                else:
                    screen.blit(self.images[self.map[y][x]], (x*GS-offsetx,y*GS-offsety))
        # このマップにいるキャラクターを描画
        for chara in self.charas:
            chara.draw(screen, offset)
    def is_movable(self, x, y):
        """(x,y)は移動可能か？"""
        # マップ範囲内か？
        if x < 0 or x > self.col-1 or y < 0 or y > self.row-1:
            return False
        # マップチップは移動可能か？
        if self.map[y][x] == 1 or self.map[y][x] == 4:  # 水と山は移動できない
            return False
        # キャラクターと衝突しないか？
        for chara in self.charas:
            if chara.x == x and chara.y == y:
                return False
        return True
    def load(self):
        """ファイルからマップをロード"""
        file = os.path.join("data", self.name + ".map")
        # テキスト形式のマップを読み込む
        fp = open(file)
        lines = fp.readlines()
        row_str, col_str = lines[0].split()  # 行数と列数
        self.row, self.col = int(row_str), int(col_str)
        self.default = int(lines[1])  # デフォルト値
        for line in lines[2:]:
            line = line.rstrip()
            self.map.append([int(x) for x in list(line)])
        fp.close()
    def load_event(self):
        """ファイルからイベントをロード"""
        file = os.path.join("data", self.name + ".evt")
        # テキスト形式のイベントを読み込む
        fp = codecs.open(file, "r", "utf-8")
        for line in fp:
            line = line.rstrip()  # 改行除去
            if line.startswith("#"): continue  # コメント行は無視
            data = line.split(",")
            event_type = data[0]
            if event_type == "CHARA":  # キャラクターイベント
                self.create_chara(data)
        fp.close()
    def create_chara(self, data):
        """キャラクターを作成してcharasに追加する"""
        name = data[1]
        x, y = int(data[2]), int(data[3])
        direction = int(data[4])
        movetype = int(data[5])
        message = data[6]
        chara = Character(name, (x,y), direction, movetype, message)
        self.charas.append(chara)

class Character:
    """一般キャラクタークラス"""
    speed = 4  # 1フレームの移動ピクセル数
    animcycle = 24  # アニメーション速度
    frame = 0
    # キャラクターイメージ（mainで初期化）
    # キャラクター名 -> 分割画像リストの辞書
    images = {}
    def __init__(self, name, pos, dir, movetype, message):
        self.name = name  # プレイヤー名（ファイル名と同じ）
        self.image = self.images[name][0]  # 描画中のイメージ
        self.x, self.y = pos[0], pos[1]  # 座標（単位：マス）
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.vx, self.vy = 0, 0  # 移動速度
        self.moving = False  # 移動中か？
        self.direction = dir  # 向き
        self.movetype = movetype  # 移動タイプ
        self.message = message  # メッセージ
    def update(self, map):
        """キャラクター状態を更新する。
        mapは移動可能かの判定に必要。"""
        # プレイヤーの移動処理
        if self.moving == True:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # マスにおさまったら移動完了
                self.moving = False
                self.x = self.rect.left / GS
                self.y = self.rect.top / GS
        elif self.movetype == MOVE and random.random() < PROB_MOVE:
            # 移動中でないならPROB_MOVEの確率でランダム移動開始
            self.direction = random.randint(0, 3)  # 0-3のいずれか
            if self.direction == DOWN:
                if map.is_movable(self.x, self.y+1):
                    self.vx, self.vy = 0, self.speed
                    self.moving = True
            elif self.direction == LEFT:
                if map.is_movable(self.x-1, self.y):
                    self.vx, self.vy = -self.speed, 0
                    self.moving = True
            elif self.direction == RIGHT:
                if map.is_movable(self.x+1, self.y):
                    self.vx, self.vy = self.speed, 0
                    self.moving = True
            elif self.direction == UP:
                if map.is_movable(self.x, self.y-1):
                    self.vx, self.vy = 0, -self.speed
                    self.moving = True
        # キャラクターアニメーション（frameに応じて描画イメージを切り替える）
        self.frame += 1
        self.image = self.images[self.name][self.direction*4+self.frame/self.animcycle%4]
    def draw(self, screen, offset):
        """オフセットを考慮してプレイヤーを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
    def __str__(self):
        return "CHARA,%s,%d,%d,%d,%d,%s" % (self.name,self.x,self.y,self.direction,self.movetype,self.message)

class Player(Character):
    """プレイヤークラス"""
    def __init__(self, name, pos, dir):
        Character.__init__(self, name, pos, dir, False, None)
    def update(self, map):
        """プレイヤー状態を更新する。
        mapは移動可能かの判定に必要。"""
        # プレイヤーの移動処理
        if self.moving == True:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # マスにおさまったら移動完了
                self.moving = False
                self.x = self.rect.left / GS
                self.y = self.rect.top / GS
                # TODO: ここに接触イベントのチェックを入れる
        else:
            # プレイヤーの場合、キー入力があったら移動を開始する
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_DOWN]:
                self.direction = DOWN  # 移動できるかに関係なく向きは変える
                if map.is_movable(self.x, self.y+1):
                    self.vx, self.vy = 0, self.speed
                    self.moving = True
            elif pressed_keys[K_LEFT]:
                self.direction = LEFT
                if map.is_movable(self.x-1, self.y):
                    self.vx, self.vy = -self.speed, 0
                    self.moving = True
            elif pressed_keys[K_RIGHT]:
                self.direction = RIGHT
                if map.is_movable(self.x+1, self.y):
                    self.vx, self.vy = self.speed, 0
                    self.moving = True
            elif pressed_keys[K_UP]:
                self.direction = UP
                if map.is_movable(self.x, self.y-1):
                    self.vx, self.vy = 0, -self.speed
                    self.moving = True
        # キャラクターアニメーション（frameに応じて描画イメージを切り替える）
        self.frame += 1
        self.image = self.images[self.name][self.direction*4+self.frame/self.animcycle%4]

class Window:
    """ウィンドウの基本クラス"""
    EDGE_WIDTH = 4  # 白枠の幅
    def __init__(self, rect):
        self.rect = rect  # 一番外側の白い矩形
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH*2, -self.EDGE_WIDTH*2)  # 内側の黒い矩形
        self.is_visible = False  # ウィンドウを表示中か？
    def draw(self, screen):
        """ウィンドウを描画"""
        if self.is_visible == False: return
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)
    def show(self):
        """ウィンドウを表示"""
        self.is_visible = True
    def hide(self):
        """ウィンドウを隠す"""
        self.is_visible = False

if __name__ == "__main__":
    main()
