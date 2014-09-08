#!/usr/bin/env python
#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

earth_angle = 0.0
moon_angle = 0.0

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("惑星")
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
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    # 太陽の描画
    glColor3f(1.0, 0.0, 0.0)
    glutSolidSphere(1.0, 50, 50)
    
    # 地球の描画
    glRotatef(earth_angle, 0.0, 1.0, 0.0)
    glTranslatef(2.5, 0.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glutSolidSphere(0.2, 20, 20)
    
    # 月の描画
    glColor3f(1.0, 1.0, 0.0)
    glRotatef(moon_angle, 0.0, 1.0, 0.0)
    glTranslatef(0.5, 0.0, 0.0)
    glutSolidSphere(0.1, 20, 20)
    
    glutSwapBuffers()
    
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, width/height, 1.0, 20.0)
    glMatrixMode(GL_MODELVIEW)

def idle():
    global earth_angle, moon_angle
    earth_angle += 0.01  # 地球の回転角を更新
    moon_angle += 0.1    # 月の回転角を更新
    glutPostRedisplay()

if __name__ == "__main__":
    main()
