# Código desenvolvido em conjunto por Leonardo Izaú e Mariana Fortes.
# O arquivo ply.py foi importado do repositório de Conrado Luiz, disponível em: <https://github.com/ConradoLuiz/computacao-grafica/tree/master/FlightSimulator>
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from ply import *

def display():
    global coelho
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(2,1,3,0)
    coelho.draw()
    glutSwapBuffers()

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,20.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.8,0.0,0.3,0,0,0,0,1,0)

def init():
    global coelho

    glLightfv(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.05, 0.05, 0.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    coelho = PlyReader("bun_zipper.ply")

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Coelho")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()
