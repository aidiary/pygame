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
    glutCreateWindow("神々のトライフォース")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutMainLoop()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    glRotatef(angle, 0.0, 1.0, 0.0)
    draw_triforce()
    
    glutSwapBuffers()

def draw_triforce():
    """トライフォースを描画"""
    glColor3f(1.0, 1.0, 0.0)
    
    glBegin(GL_TRIANGLES)
    # 上の三角形
    glVertex2f(0, 0.8)
    glVertex2f(-0.4, 0.0)
    glVertex2f(0.4, 0.0)
    # 左下の三角形
    glVertex2f(-0.4, 0.0)
    glVertex2f(-0.8, -0.8)
    glVertex2f(0.0, -0.8)
    # 右下の三角形
    glVertex2f(0.4, 0.0)
    glVertex2f(0.0, -0.8)
    glVertex2f(0.8, -0.8)
    glEnd()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, width/height, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def idle():
    global angle
    angle += 0.05
    glutPostRedisplay()

if __name__ == "__main__":
    main()
