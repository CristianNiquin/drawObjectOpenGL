import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from functionGL import *
from loadFiles2 import *
import math, sys, glm
import numpy as np

class Objeto(object):
    def __init__(self, _data, _image):
        self.data = _data
        self.image = _image

        self.list_VAO = list()
        self.list_Model = list()
        self.TEX = None
        self.programId = 0

        # MODEL-VIEW-PROJECTION MATRIX
        self.Projection = glm.perspective(glm.radians(60.0), 4.0 / 3.0, 0.1, 100.0)
        self.View = glm.mat4(glm.lookAt(glm.vec3(0, 0, 7), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0)))

        for i in range(len(self.data.vaos)):
            self.list_Model.append(glm.mat4(1.0))

        self.falange = 19

    def loadData(self):
        VBO = glGenBuffers(len(self.data.vaos))

        for i, dot in enumerate(self.data.vaos):
            VAO = glGenVertexArrays(1)
            
            glBindVertexArray(VAO)                      # LINK 'VAO' ARRAY  
            glBindBuffer(GL_ARRAY_BUFFER, VBO[i])       # LINK 'VBO' TO BUFFER
            
            # STORE VERTEX IN BUFFER -> (-, num bytes, reference, -)
            glBufferData(GL_ARRAY_BUFFER, dot.nbytes, dot, GL_STATIC_DRAW)
            
            # STORE VERTEX IN ARRAY -> (index layout, type, normalized, strid, pointer)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
            glEnableVertexAttribArray(1)

            self.list_VAO.append(VAO)
        
        self.TEX = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.TEX)      # LINK 'TEX'

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
        self.moveHand()

        glutSwapBuffers()

    def keyboard(self, k, x, y):
        key = k.decode("utf-8")
        if key == 'q':
            sys.exit()
        elif key == '0':
            self.falange = 19
        elif key == '1':
            self.falange = 0
        elif key == '2':
            self.falange = 4
        elif key == '3':
            self.falange = 8
        elif key == '4':
            self.falange = 12
        elif key == '5':
            self.falange = 16
        elif key == '6':
            self.falange = 1
        elif key == '7':
            self.falange = 5
        elif key == '7':
            self.falange = 9
        elif key == '9':
            self.falange = 13
        
        glutPostRedisplay()

    def moveHand(self):

        self.moveObject(19, 1)
        self.moveFalange()

    def moveFalange(self):
        self.moveObject(0, 4)
        self.moveObject(4, 4)
        self.moveObject(8, 4)
        self.moveObject(12, 4)
        self.moveObject(16, 3)
    
    def moveObject(self, index, value):
        if value==0:
            return
        else:        
            if index == self.falange:
                self.list_Model[index] = glm.rotate(self.list_Model[index], 0.03141592, glm.vec3(1.0, 0.0, 0.0))

            glBindVertexArray(self.list_VAO[index])

            MVP = self.Projection * self.View * self.list_Model[index]
            MVP = np.array(MVP, dtype = np.float32)

            # GET AND SET MATRIX MVP TO SHADER
            matrixId = glGetUniformLocation(self.programId, 'MVP')
            glUniformMatrix4fv(matrixId, 1, GL_FALSE, MVP)
            glDrawArrays(GL_TRIANGLES, 0, len(self.data.vaos[index]))

            self.moveObject(index+1, value-1)


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