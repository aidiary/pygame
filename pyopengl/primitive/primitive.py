#!/usr/bin/env python
#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("プリミティブの描画")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

def init():
    glClearColor(0.0, 0.0, 1.0, 1.0)
    
    # 座標系の設定
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT)
    
    # 赤い四角形ポリゴンを描く
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glEnd()
    
    glFlush()

if __name__ == "__main__":
    main()
