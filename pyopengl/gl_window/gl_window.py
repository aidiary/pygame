#!/usr/bin/env python
#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(300, 300)  # ウィンドウサイズ
    glutInitWindowPosition(100, 100)  # ウィンドウ位置
    glutCreateWindow("OpenGLウィンドウの表示")  # ウィンドウを表示
    glutDisplayFunc(display)  # 描画関数を登録
    init()
    glutMainLoop()

def init():
    glClearColor(0.0, 0.0, 1.0, 1.0)

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT)  # 画面のクリア
    glFlush()  # OpenGLコマンドの強制実行

if __name__ == "__main__":
    main()
