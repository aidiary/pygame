#!/usr/bin/env python
#coding:utf-8
import pygame
from pygame.locals import *
import os
import struct
import sys
import codecs

SCR_RECT = Rect(0, 0, 800, 640)
INPUT_RECT = Rect(240, 302, 320, 36)
GS = 32

show_grid = False  # グリッドを表示するか？

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"PyMap 06 マップの保存")
    
    # マップチップをロード
    load_mapchips("data", "mapchip.dat")
    
    palette = MapchipPalette()
    map = Map("NEW", 64, 64, 5, palette)
    cursor = Cursor(0, 0)
    msg_engine = MessageEngine()
    input_wnd = InputWindow(INPUT_RECT, msg_engine)
    
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
            # 選択マップチップを左上に描画
            screen.blit(Map.images[palette.selected_mapchip], (10,10))
            pygame.draw.rect(screen, (0,255,0), (10,10,32,32), 3)
            # マウスの座標を描画
            px, py = pygame.mouse.get_pos()
            selectx = (px + offset[0]) / GS
            selecty = (py + offset[1]) / GS
            msg_engine.draw_string(screen, (10,56), map.name)
            msg_engine.draw_string(screen, (10,86), u"%d　%d" % (selectx, selecty))
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
            elif event.type == KEYDOWN and event.key == K_g:
                # グリッドの表示/非表示を切り替え
                global show_grid  # show_gridはグローバル変数
                show_grid = not show_grid
            elif event.type == KEYDOWN and event.key == K_n:
                # 新規マップ
                try:
                    name = input_wnd.ask(screen, "NAME?")
                    row = int(input_wnd.ask(screen, "ROW?"))
                    col = int(input_wnd.ask(screen, "COL?"))
                    default = int(input_wnd.ask(screen, "DEFAULT?"))
                except ValueError:
                    print "Cannot create map"
                    continue
                map = Map(name, row, col, default, palette)
            elif event.type == KEYDOWN and event.key == K_s:
                # マップをセーブ
                name = input_wnd.ask(screen, "SAVE?")
                map.save(name)

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
    def __init__(self, name, row, col, default, palette):
        self.name = name
        self.row = row
        self.col = col
        self.default = default  # デフォルトのマップチップ番号
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
                    if show_grid:
                        pygame.draw.rect(screen, (0,0,0), (x*GS-offsetx,y*GS-offsety,GS,GS), 1)
    def save(self, name):
        """マップをバイナリ形式でfileに保存"""
        file = "%s.map" % (name.lower())
        fp = open(file, "wb")  # バイナリモードで開く
        # 行数、列数はi(int)で保存
        fp.write(struct.pack("i", self.row))
        fp.write(struct.pack("i", self.col))
        # マップチップはB(unsigned char)で保存
        # 8bitなのでマップチップは256種類まで
        fp.write(struct.pack("B", self.default))
        for r in range(self.row):
            for c in range(self.col):
                fp.write(struct.pack("B", self.map[r][c]))
        fp.close()

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

def load_image(dir, file, colorkey=None):
    file = os.path.join(dir, file)
    try:
        image = pygame.image.load(file)
    except pygame.error, message:
        print "Cannot load image:", file
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

def load_mapchips(dir, file):
    """マップチップをロードしてMap.imagesに格納"""
    file = os.path.join(dir, file)
    fp = open(file, "r")
    for line in fp:
        line = line.rstrip()  # 改行除去
        data = line.split(",")  # カンマで分解
        id = int(data[0])  # マップチップID
        name = data[1]  # マップチップ名
        movable = int(data[2])  # 移動可能か？（エディタでは未使用）
        Map.images.append(load_image("mapchip", "%s.png" % name))
    fp.close()

class MessageEngine:
    FONT_WIDTH = 16
    FONT_HEIGHT = 22
    WHITE, RED, GREEN, BLUE = 0, 160, 320, 480
    def __init__(self):
        self.image = load_image("data", "font.png", -1)
        self.color = self.WHITE
        self.kana2rect = {}
        self.create_hash()
    def set_color(self, color):
        """文字色をセット"""
        self.color = color
        # 変な値だったらWHITEにする
        if not self.color in [self.WHITE,self.RED,self.GREEN,self.BLUE]:
            self.color = self.WHITE
    def draw_character(self, screen, pos, ch):
        """1文字だけ描画する"""
        x, y = pos
        try:
            rect = self.kana2rect[ch]
            screen.blit(self.image, (x,y), (rect.x+self.color,rect.y,rect.width,rect.height))
        except KeyError:
            print "描画できない文字があります:%s" % ch
            return
    def draw_string(self, screen, pos, str):
        """文字列を描画"""
        x, y = pos
        for i, ch in enumerate(str):
            dx = x + self.FONT_WIDTH * i
            self.draw_character(screen, (dx,y), ch)
    def create_hash(self):
        """文字から座標への辞書を作成"""
        filepath = os.path.join("data", "kana2rect.dat")
        fp = codecs.open(filepath, "r", "utf-8")
        for line in fp.readlines():
            line = line.rstrip()
            d = line.split(" ")
            kana, x, y, w, h = d[0], int(d[1]), int(d[2]), int(d[3]), int(d[4])
            self.kana2rect[kana] = Rect(x, y, w, h)
        fp.close()

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

class InputWindow(Window):
    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.msg_engine = msg_engine
    def get_key(self):
        """キー入力を読み取る"""
        while True:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass
    def draw(self, screen, message):
        Window.draw(self, screen)
        if len(message) != 0:
            self.msg_engine.draw_string(screen, self.inner_rect.topleft, message)
            pygame.display.flip()
    def ask(self, screen, question):
        cur_str = []
        self.show()
        self.draw(screen, question)
        while True:
            key = self.get_key()
            if key == K_BACKSPACE:
                cur_str = cur_str[0:-1]
            elif key == K_ESCAPE:
                return None
            elif key == K_RETURN:
                break
            elif K_0 <= key <= K_9 or K_a <= key <= K_z:
                cur_str.append(chr(key).upper())
            self.draw(screen, question + u"　" + "".join(cur_str))
        return "".join(cur_str)

if __name__ == "__main__":
    main()
