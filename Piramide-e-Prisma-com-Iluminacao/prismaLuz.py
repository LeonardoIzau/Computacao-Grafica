#Código desenvolvido em conjunto por Leonardo Izaú e Mariana Fortes.

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import math
import sys

#Recebe do usuário o número de arestas da base
''' 
if len(sys.argv) >= 2:
    n = int(sys.argv[1])
else:
	n = int(input("Digite o numero de arestas da base da piramide: "))
'''

n = 6

#Mapeamento da posição dos vértices de acordo com o número de lados
vertBase1 = []
vertBase2 = []
r = 2
a = (2*math.pi)/n
for i in range(0,n):
    x = r*math.cos(a*i)
    z = r*math.sin(a*i)
    vertBase1 += [[x,0,z]]
    vertBase2 += [[x,2,z]]
    
vertices = vertBase1 + vertBase2

#Mapeamento das bases do prisma de acordo com o número de lados
base1 = []
base2 = []
for i in range(0,n):
    base1 += [i]
    base2 += [i+n]

#Mapeamento das faces laterais de acordo com o número de lados
facesLaterais = []
for i in range(0,n):
    if(i < n-1):
        facesLaterais += [[i, i+1, i+n, i+n+1]]
    if(i == n-1):
        facesLaterais += [[i, 0, i+n, n]]

print(vertices)
print(facesLaterais)
print(base1)
print(base2)

#https://www.opengl.org/wiki/Calculating_a_Surface_Normal
#Begin Function CalculateSurfaceNormal (Input Triangle) Returns Vector
#  Set Vector U to (Triangle.p2 minus Triangle.p1)
#  Set Vector V to (Triangle.p3 minus Triangle.p1)
#  Set Normal.x to (multiply U.y by V.z) minus (multiply U.z by V.y)
#  Set Normal.y to (multiply U.z by V.x) minus (multiply U.x by V.z)
#  Set Normal.z to (multiply U.x by V.y) minus (multiply U.y by V.x)
#  Returning Normal
#End Function

def calculaNormalFace(face, tipoFace):
    x = 0
    y = 1
    z = 2
    #0 = faces laterais, 1 = base inferior, 2 = base superior
    if((tipoFace == 0) or (tipoFace == 2)):
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]
    if(tipoFace == 1):
        v0 = vertices[face[2]]
        v1 = vertices[face[1]]
        v2 = vertices[face[0]]
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)

#Função que define a forma do prisma
def Prisma():
    #Desenho e iluminação das faces laterais do prisma
    glBegin(GL_TRIANGLE_STRIP)
    i = 0
    for face in facesLaterais:
        glNormal3fv(calculaNormalFace(face, 0))
        for vertex in face:
            glVertex3fv(vertices[vertex])
        i = i + 1
    glEnd()
    
    #Desenho e iluminação da base inferior do prisma
    glBegin(GL_POLYGON)
    glNormal3fv(calculaNormalFace(base1, 1))
    for vert in base1:
        glVertex3fv(vertices[vert])
    glEnd()
    
    #Desenho e iluminação da base superior do prisma
    glBegin(GL_POLYGON)
    glNormal3fv(calculaNormalFace(base2, 2))
    for vert in base2:
        glVertex3fv(vertices[vert])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(2,0,5,5)
    Prisma()
    glutSwapBuffers()

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Camera Virtual
    #          onde    Pra onde 
    gluLookAt( 10,0,0, 0,0,0,     0,1,0 )

def init():
    mat_ambient = (0.4, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (10, 0, 0)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_SMOOTH)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Prisma")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()