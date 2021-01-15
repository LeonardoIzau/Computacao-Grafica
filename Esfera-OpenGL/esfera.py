#Código desenvolvido em conjunto por Leonardo Izaú e Mariana Fortes.

import sdl2
import math
from OpenGL.GL import *
from OpenGL.GLU import *

r = 10
theta0 = 0
phi0 = 0
thetaf = 2*math.pi
phif = math.pi
qt_theta = 50
qt_phi = 50
d_theta = (thetaf-theta0)/qt_theta
d_phi = (phif-phi0)/qt_phi

def f(r,theta,phi):
    x = r*math.cos(theta)*math.sin(phi)
    y = r*math.sin(theta)*math.sin(phi)
    z = r*math.cos(phi)
    return x,y,z

ax = 0
ay = 0

def desenha():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotate(ax,1,0,0)
    glRotate(ay,0,1,0)
    phi = phi0
    for i in range(0,qt_phi):
        theta = theta0
        glColor3f(1,1-(i/qt_phi),(i/qt_phi))
        # Começa a quad_strip
        glBegin(GL_QUAD_STRIP)
        for j in range(0,qt_theta):
            # emitir o vertice 2j
            x,y,z = f(r,theta,phi)
            glVertex3f(x,y,z)
            # emitir o vertice 2j+1
            x,y,z = f(r,theta,phi+d_phi)
            glVertex3f(x,y,z)
            theta += d_theta
        x,y,z = f(r, thetaf, phi)
        glVertex3f(x,y,z)
        x,y,z = f(r,thetaf,phi+d_phi)
        glVertex3f(x,y,z)
        glEnd()
        phi += d_phi
    glPopMatrix()

#Função desenvolvida com ajuda do código desenvolvido pelo Vispy Development Team, disponível no link <https://programtalk.com/vs2/python/13762/vispy/vispy/app/backends/_sdl2.py/>.
def getPosicaoPonteiro():
        x, y = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        return y.value, x.value

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 0)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetSwapInterval(1)
window = sdl2.SDL_CreateWindow(b"Esfera", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
if not window:
    sys.stderr.write("Error: Could not create window\n")
    exit(1)
glcontext = sdl2.SDL_GL_CreateContext(window)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,800.0/600.0,0.1,200.0)
glTranslatef(0.0,0.0,-60)

running = True
event = sdl2.SDL_Event()
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
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
        if (event.type == sdl2.SDL_MOUSEMOTION):
            ax, ay = getPosicaoPonteiro()
        
    desenha()
    sdl2.SDL_GL_SwapWindow(window)