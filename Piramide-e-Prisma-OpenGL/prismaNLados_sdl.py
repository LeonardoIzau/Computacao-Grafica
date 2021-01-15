#Código desenvolvido em conjunto por Leonardo Izaú e Mariana Fortes.

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys
import sdl2
import math

#Recebe do usuário o número de arestas das bases 
if len(sys.argv) >= 2:
    n = int(sys.argv[1])
else:
	n = int(input("Digite o numero de arestas da base do prisma: "))

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

#Mapeamento das arestas de acordo com as coordenadas dos vértices e o número de lados
linhas = []
for i in range(0,n):
    if(i < n-1): 
        linhas += [[i, i+1]]
    if(i == n-1):
        linhas += [[i, 0]]
for i in range(n,2*n):
    if(i < (2*n-1)):
        linhas += [[i, i+1]]
    if(i == (2*n-1)):
        linhas += [[i, n]]
for i in range(0,n):
    linhas += [[i, i+n]]

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

#Vetor de cores que aplica cores alternadas para cada face lateral do prisma
cores = ( (1,1,0),(0,1,0),(0,1,1),(0,0,1),(1,0,1) )
coresLaterais = []
for i in range(0, n):
    if(i <= 4):
        coresLaterais += [cores[i]]
    else:
        coresLaterais += [cores[i%5]]

#Função que define a forma do prisma
def Prisma():
    #Desenho e coloração das faces laterais do prisma
    glBegin(GL_TRIANGLE_STRIP)
    i = 0
    for face in facesLaterais:
        glColor3fv(coresLaterais[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
        i = i + 1
    glEnd()
    
    #Desenho e coloração da base inferior do prisma
    glBegin(GL_POLYGON)
    glColor3fv((1,1,1))
    for vert in base1:
        glVertex3fv(vertices[vert])
    glEnd()
    
    #Desenho e coloração da base superior do prisma
    glBegin(GL_POLYGON)
    glColor3fv((0.5,0,0))
    for vert in base2:
        glVertex3fv(vertices[vert])
    glEnd()
    
    #Desenho e coloração das arestas do prisma
    glColor3fv((0,0.5,0))
    glBegin(GL_LINES)
    for linha in linhas:
        for vertice in linha:
            glVertex3fv(vertices[vertice])
    glEnd()

#Inicialização dos ângulos de rotação do prisma
ax = 0
ay = 0

#Função que renderiza e rotaciona o prisma na tela
def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(ax,1,0,0)
    glRotatef(ay,0,1,0)
    Prisma()
    glPopMatrix()
 
#Função desenvolvida com ajuda do código desenvolvido pelo Vispy Development Team, disponível no link <https://programtalk.com/vs2/python/13762/vispy/vispy/app/backends/_sdl2.py/>.
def getPosicaoPonteiro():
        x, y = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        return y.value, x.value

#Inicialização do SDL

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 0)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetSwapInterval(1)
window = sdl2.SDL_CreateWindow(b"Prisma", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
if not window:
    sys.stderr.write("Error: Could not create window\n")
    exit(1)
glcontext = sdl2.SDL_GL_CreateContext(window)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,800.0/600.0,0.1,200.0)
glTranslatef(0.0,0.0,-10)

running = True
event = sdl2.SDL_Event()
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
        #Usa as setas do teclado para girar o prisma e a tecla ESC para fechar o programa
        if event.type == sdl2.events.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
            if event.key.keysym.sym == sdl2.SDLK_DOWN:
                ax += 5
            if event.key.keysym.sym == sdl2.SDLK_UP:
                ax -= 5
            if event.key.keysym.sym == sdl2.SDLK_LEFT:
                ay += 5
            if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                ay -= 5
        #Usa a posição do mouse para girar o prisma
        if (event.type == sdl2.SDL_MOUSEMOTION):
            ax, ay = getPosicaoPonteiro()
    desenha()
    sdl2.SDL_GL_SwapWindow(window)
