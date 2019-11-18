from OpenGL.GL import *
from OpenGL.GL.shaders import *
from PIL import Image
import numpy as np

# COMPILE SHADERS
def compileShaders(shaderFile, shaderType):
    shaderId = glCreateShader(shaderType)
    glShaderSource(shaderId, shaderFile)

    glCompileShader(shaderId)
    glGetShaderiv(shaderId, GL_COMPILE_STATUS)

    return shaderId

# LINK SHADERS TO PROGRAM
def linkProgram(vertexShaderId, fragmentShaderId):
    program = glCreateProgram()

    glAttachShader(program, vertexShaderId)
    glAttachShader(program, fragmentShaderId)

    glLinkProgram(program)
    glGetProgramiv(program, GL_LINK_STATUS)

    return program

# LOAD TEXTURES
def loadTexture(textureFile):
    image = Image.open(textureFile).transpose( Image.FLIP_TOP_BOTTOM )
    width, height = image.size[0], image.size[1]
    img = np.array(list(image.getdata()), np.uint8)

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    # COPY THE TEXTURE DATA INTO 'TEX'
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
    glGenerateMipmap(GL_TEXTURE_2D)

    image.close()

#
def defDepth(cR, cG, cB):
    # FUNTION DEPTH
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glClearDepth(1.0)
    glClearColor(cR, cG, cB, 0.0)
