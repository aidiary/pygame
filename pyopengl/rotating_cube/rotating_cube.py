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
    glutCreateWindow("回転キューブ")
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
    glLoadIdentity()

    gluLookAt(3.0, 2.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotatef(angle, 3.0, 2.0, 1.0)
    draw_cube()  # 立方体を描く
    
    glutSwapBuffers()

def reshape(width, height):
    """画面サイズの変更時に呼び出されるコールバック関数"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

def idle():
    """アイドル時に呼ばれるコールバック関数"""
    global angle
    angle += 0.05  # 角度を更新
    glutPostRedisplay()  # 再描画

def draw_cube():
    """立方体を描く"""
#   glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glBegin(GL_QUADS)
    # 上面（緑）
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)   # A
    glVertex3f(-1.0, 1.0, -1.0)  # B
    glVertex3f(-1.0, 1.0, 1.0)   # C
    glVertex3f(1.0, 1.0, 1.0)    # D
    # 下面（オレンジ）
    glColor3f(1, 0.5, 0)
    glVertex3f(1.0, -1.0, -1.0)  # E
    glVertex3f(-1.0, -1.0, -1.0) # F
    glVertex3f(-1.0, -1.0, 1.0)  # G
    glVertex3f(1.0, -1.0, 1.0)   # H
    # 前面（赤）
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)    # D
    glVertex3f(-1.0, 1.0, 1.0)   # C
    glVertex3f(-1.0, -1.0, 1.0)  # G
    glVertex3f(1.0, -1.0, 1.0)   # H
    # 背面（黄色）
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)   # A
    glVertex3f(-1.0, 1.0, -1.0)  # B
    glVertex3f(-1.0, -1.0, -1.0) # F
    glVertex3f(1.0, -1.0, -1.0)  # E
    # 左側面（青）
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)   # C
    glVertex3f(-1.0, 1.0, -1.0)  # B
    glVertex3f(-1.0, -1.0, -1.0) # F
    glVertex3f(-1.0, -1.0, 1.0)  # G
    # 右側面（マゼンタ）
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)    # D
    glVertex3f(1.0, 1.0, -1.0)   # A
    glVertex3f(1.0, -1.0, -1.0)  # E
    glVertex3f(1.0, -1.0, 1.0)   # H
    glEnd()

if __name__ == "__main__":
    main()
