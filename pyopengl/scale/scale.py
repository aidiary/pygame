#!/usr/bin/env python
#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

angle = 0.0

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("拡大縮小")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    init(300, 300)
    glutMainLoop()

def init(width, height):
    """初期化"""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    # カメラは原点でZの負の方向を撮影（デフォルト）
    
    # 赤いTeapot
    glLoadIdentity()
    glTranslatef(-2.0, 0.0, -10.0)   # 平行移動
    glRotatef(angle, 0.0, 1.0, 0.0)  # 回転
    glScale(1.0, 0.5, 1.0)           # 縮小
    glColor3f(1.0, 0.0, 0.0)
    glutSolidTeapot(1.0)
    
    # 青いTeapot
    glLoadIdentity()
    glTranslatef(2.0, 0.0, -10.0)    # 平行移動
    glRotatef(angle, 1.0, 0.0, 0.0)  # 回転
    glScale(1.0, 3.0, 1.0)           # 拡大
    glColor3f(0.0, 0.0, 1.0)
    glutSolidTeapot(1.0)

    glutSwapBuffers()

def idle():
    """アイドル時に呼ばれるコールバック関数"""
    global angle
    angle += 2.0  # 角度を更新
    glutPostRedisplay()  # 再描画

def reshape(width, height):
    """画面サイズの変更時に呼ばれるコールバック関数"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
