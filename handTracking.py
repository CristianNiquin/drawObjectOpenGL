import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from functionGL import *
from loadFilesVaos import *
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

        self.falange = -1
        self.dir = 1
        self.x = 1.0; self.y = 0.0; self.z = 0.0

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
        self.moveObject(19, 1, False)

        glutSwapBuffers()

    def keyboard(self, k, x, y):
        key = k.decode("utf-8")
        if key == '+':
            self.x *= -1.0; self.y *= -1.0; self.z *= -1.0
            self.falange = -1
        elif key == 'a':
            self.falange = 1
        elif key == 's':
            self.falange = 2
        elif key == 'd':
            self.falange = 3
        elif key == 'f':
            self.falange = 5
        elif key == 'g':
            self.falange = 6
        elif key == 'h':
            self.falange = 7
        elif key == 'j':
            self.falange = 9
        elif key == 'k':
            self.falange = 10
        elif key == 'l':
            self.falange = 11
        elif key == 'c':
            self.falange = 13
        elif key == 'v':
            self.falange = 14
        elif key == 'b':
            self.falange = 15
        elif key == 'n':
            self.falange = 17
        elif key == 'm':
            self.falange = 18
        elif key == 'x':
            self.x = 1.0; self.y = 0.0; self.z = 0.0
            self.falange = 19
        elif key == 'y':
            self.x = 0.0; self.y = 1.0; self.z = 0.0
            self.falange = 19
        elif key == 'z':
            self.x = 0.0; self.y = 0.0; self.z = 1.0
            self.falange = 19
        else:
            self.falange = -1
        glutPostRedisplay()

    def moveFalange(self, active):
        self.moveObject(0, 4, active)
        self.moveObject(4, 4, active)
        self.moveObject(8, 4, active)
        self.moveObject(12, 4, active)
        self.moveObject(16, 3, active)
    
    def moveObject(self, index, value, active):
        if value==0:
            return
        else:        
            if index == self.falange or active == True:
                self.list_Model[index] = glm.rotate(self.list_Model[index], 0.03141592, glm.vec3(self.x, self.y, self.z))
                active = True

            glBindVertexArray(self.list_VAO[index])

            MVP = self.Projection * self.View * self.list_Model[index]
            MVP = np.array(MVP, dtype = np.float32)

            # GET AND SET MATRIX MVP TO SHADER
            matrixId = glGetUniformLocation(self.programId, 'MVP')
            glUniformMatrix4fv(matrixId, 1, GL_FALSE, MVP)
            glDrawArrays(GL_TRIANGLES, 0, len(self.data.vaos[index]))

            if index == 19:
                self.moveFalange(active)
            else:
                self.moveObject(index+1, value-1, active)


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