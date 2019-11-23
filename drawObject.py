import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from functionGL import *
from loadFiles import *
import math, sys, glm
import numpy as np

class Objeto(object):
    def __init__(self, _data, _image):
        self.data = _data
        self.image = _image

        self.VBO = None
        self.VAO = None
        self.EBO = None
        self.TEX = None
        self.programId = 0

        # MODEL-VIEW-PROJECTION MATRIX
        self.Projection = glm.perspective(glm.radians(60.0), 4.0 / 3.0, 0.1, 100.0)
        self.View = glm.mat4(glm.lookAt(glm.vec3(0, 0, 7), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0)))
        self.Model = glm.mat4(1.0)
        self.MVP = self.Projection * self.View * self.Model
        self.MVP = np.array(self.MVP, dtype = np.float32)

    def loadData(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)                 # LINK 'VAO' ARRAY  

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)     # LINK 'VBO' TO BUFFER

        self.TEX = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.TEX)      # LINK 'TEX'

        # STORE VERTEX IN BUFFER -> (-, num bytes, reference, -)
        glBufferData(GL_ARRAY_BUFFER, self.data.dot.nbytes, self.data.dot, GL_STATIC_DRAW)
        # STORE VERTEX IN ARRAY -> (index layout, type, normalized, strid, pointer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        # STORE AND LOAD TEXTURE
        loadTexture(self.image)

        # UNLINK VAO-VBO-EBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def init(self):
        defDepth(0.0, 0.0, 0.0)
        self.loadData()

        # COMPILE SHADERS
        vShaderId = compileShaders(self.data.vShader, GL_VERTEX_SHADER)
        fShaderId = compileShaders(self.data.fShader, GL_FRAGMENT_SHADER)
        # LINK SHADERS TO PROGRAM
        self.programId = linkProgram(vShaderId, fShaderId)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # ACTIVE PROGRAM
        glUseProgram(self.programId)
        glBindVertexArray(self.VAO)

        # GET AND SET MATRIX MVP TO SHADER
        matrixId = glGetUniformLocation(self.programId, 'MVP')
        glUniformMatrix4fv(matrixId, 1, GL_FALSE, self.MVP)
        glDrawArrays(GL_TRIANGLES, 0, len(self.data.face))

        glutSwapBuffers()

    def keyboard(self, k, x, y):
        key = k.decode("utf-8")
        if key == 'q':
            sys.exit()
        elif key == 'x':
            self.Model = glm.rotate(self.Model, 0.03141592, glm.vec3(1.0, 0.0, 0.0))
        elif key == 'y':
            self.Model = glm.rotate(self.Model, 0.03141592, glm.vec3(0.0, 1.0, 0.0))
        elif key == 'z':
            self.Model = glm.rotate(self.Model, 0.03141592, glm.vec3(0.0, 0.0, 1.0))
        elif key == 'i':
            self.Model = glm.rotate(self.Model, 0.03141592, glm.vec3(-1.0, 0.0, 0.0))
        elif key == 'j':
            self.Model = glm.rotate(self.Model, 0.03141592, glm.vec3(0.0, -1.0, 0.0))
        elif key == 'k':
            self.Model = glm.rotate(self.Model, 0.03141592, glm.vec3(0.0, 0.0, -1.0))
        elif key == '1':
            self.Model = glm.translate(self.Model, glm.vec3(-0.1, 0, 0))
        elif key == '2':
            self.Model = glm.translate(self.Model, glm.vec3(0, -0.1, 0))
        elif key == '3':
            self.Model = glm.translate(self.Model, glm.vec3(0.1, 0, 0))
        elif key == '4':
            self.Model = glm.translate(self.Model, glm.vec3(0, 0, -0.1))
        elif key == '5':
            self.Model = glm.translate(self.Model, glm.vec3(0, 0.1, 0))
        elif key == '6':
            self.Model = glm.translate(self.Model, glm.vec3(0, 0, 0.1))
        elif key == '7':
            self.Model = glm.scale(self.Model, glm.vec3(0.1, 0.1, 0.1))
        elif key == '9':
            self.Model = glm.scale(self.Model, glm.vec3(-0.1, -0.1, -0.1))
        
        self.MVP = self.Projection * self.View * self.Model
        self.MVP = np.array(self.MVP, dtype = np.float32)
        
        glutPostRedisplay()

data = CPN("shader/vsObj.vs", "shader/fsObj.fs", "data/Hand.txt", False)
objs = Objeto(data, "Tex2.png") 

def run():
    glutInit()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
            
    glutInitWindowSize (500, 500) 
    glutInitWindowPosition (300, 200)
    glutCreateWindow("Program")
            
    objs.init()
    glutDisplayFunc(objs.display) 
    glutKeyboardFunc(objs.keyboard)

    glutMainLoop() 

run()