#!/usr/bin/env python
#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(300, 300)  # ウィンドウサイズ
    glutInitWindowPosition(100, 100)  # ウィンドウ位置
    glutCreateWindow("ティーポット")  # ウィンドウを表示
    glutDisplayFunc(display)  # 描画コールバック関数を登録
    glutReshapeFunc(reshape)  # リサイズコールバック関数の登録
    init(300, 300)
    glutMainLoop()

def init(width, height):
    """初期化"""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)  # 隠面消去を有効に

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)  # 投影変換

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # 視野変換：カメラの位置と方向のセット
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    # ティーポットを描画
    glColor3f(1.0, 0.0, 0.0)
    glutSolidTeapot(1.0)
#    glutWireTeapot(1.0)
    
    # 立方体を描画
#    glColor3f(1.0, 1.0, 0.0)
#    glutWireCube(2.0)
    
    # 球を描画
#    glColor3f(0.0, 0.0, 1.0)
#    glutWireSphere(1.0, 30, 30)
    
    glFlush()  # OpenGLコマンドの強制実行

def reshape(width, height):
    """画面サイズの変更時に呼び出されるコールバック関数"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
