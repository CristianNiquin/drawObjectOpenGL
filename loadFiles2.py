import numpy as np
import random as rd

class CPN(object):

    def __init__(self, vs, fs, file, texture):
        self.texture = list()   # VECTOR DE PUNTOS DE TEXTURA (u,v)
        self.normal = list()    # VECTOR DE NORMALES
        self.vertex = list()    # VECTOR DE PUNTOS DE COORDENADA (x,y,z)

        self.vaos = list()
        self.ebos = list()

        self.vShader = self.loadShader(vs)  # SHADER VERTICES
        self.fShader = self.loadShader(fs)  # SHADER FRAGMENT

        self.loadData(file, texture)

        self.vertex = np.array(self.vertex, dtype=np.float32)
        self.normal = np.array(self.normal, dtype=np.float32)
        self.texture = np.array(self.texture, dtype=np.float32)

    def loadData(self, file, texture):
        archivo = open(file, "r")
        # LEE EL ARCHIVO .obj
        linea = archivo.readline()
        bandera = False

        dot = list()
        face = list()

        while linea:    
            elements = linea.split()

            if len(elements) != 0 and elements[0] == 's':
                if bandera:
                    self.vaos.append( np.array(dot, dtype=np.float32) )
                    self.ebos.append( np.array(face, dtype=np.uint32) )
                    dot.clear()
                    face.clear()
                else:
                    bandera = True
            # LEE LOS VERTICES - COORDENADA
            elif len(elements) != 0 and elements[0] == 'v':
                self.vertex.append([float(elements[1]), float(elements[2]), float(elements[3])])
            
            # LEE LOS VERTICES - TEXTURA
            elif len(elements) != 0 and elements[0] == 'vt':
                self.texture.append([float(elements[1]), float(elements[2])])
            
            # LEE LOS VERTICES - NORMALES
            elif len(elements) != 0 and elements[0] == 'vn':
                self.normal.append([float(elements[1]), float(elements[2]), float(elements[3])])
            
            # LEE LAS CARAS - TRIANGULOS - v/vt/vn
            elif len(elements) != 0 and elements[0] == 'f' and texture == True:
                fa1 = int(elements[1])-1
                fa2 = int(elements[4])-1
                fa3 = int(elements[7])-1
                
                vt1 = int(elements[2])-1
                vt2 = int(elements[5])-1
                vt3 = int(elements[8])-1
                
                #vn1 = int(elements[3])-1
                #vn2 = int(elements[6])-1
                #vn3 = int(elements[9])-1
                
                # AGREGA LOS INDICES DE LAS COORDENADAS DE UNA CARA
                face.append(fa1), face.append(fa2), face.append(fa3)#, self.face.append(fa4)

                # AGREGA LAS COORDENADAS SEGUN LOS INDICES DEL VERTICE 'fa'
                # PARA LOS VERTICES Y TEXTURAS
                dot.append(self.vertex[fa1][0]), dot.append(self.vertex[fa1][1]), dot.append(self.vertex[fa1][2])
                dot.append(self.texture[vt1][0]), dot.append(self.texture[vt1][1]) 

                dot.append(self.vertex[fa2][0]), dot.append(self.vertex[fa2][1]), dot.append(self.vertex[fa2][2])
                dot.append(self.texture[vt2][0]), dot.append(self.texture[vt2][1]) 

                dot.append(self.vertex[fa3][0]), dot.append(self.vertex[fa3][1]), dot.append(self.vertex[fa3][2])
                dot.append(self.texture[vt3][0]), dot.append(self.texture[vt3][1]) 
            
            elif len(elements) != 0 and elements[0] == 'f' and texture == False:
                fa1 = int(elements[1])-1
                fa2 = int(elements[3])-1
                fa3 = int(elements[5])-1
                
                #vn1 = int(elements[2])-1
                #vn2 = int(elements[4])-1
                #vn3 = int(elements[6])-1
                
                # AGREGA LOS INDICES DE LAS COORDENADAS DE UNA CARA
                face.append(fa1), face.append(fa2), face.append(fa3)

                # AGREGA LAS COORDENADAS SEGUN LOS INDICES DEL VERTICE 'fa'
                # PARA LOS VERTICES Y TEXTURAS
                dot.append(self.vertex[fa1][0]), dot.append(self.vertex[fa1][1]), dot.append(self.vertex[fa1][2])
                dot.append(round(rd.random(),3)), dot.append(round(rd.random(),3)) 

                dot.append(self.vertex[fa2][0]), dot.append(self.vertex[fa2][1]), dot.append(self.vertex[fa2][2])
                dot.append(round(rd.random(),3)), dot.append(round(rd.random(),3)) 

                dot.append(self.vertex[fa3][0]), dot.append(self.vertex[fa3][1]), dot.append(self.vertex[fa3][2])
                dot.append(round(rd.random(),3)), dot.append(round(rd.random(),3)) 
            
            linea = archivo.readline()

        self.vaos.append( np.array(dot, dtype=np.float32) )
        self.ebos.append( np.array(face, dtype=np.uint32) )
        dot.clear()
        face.clear()
        archivo.close()

    def loadShader(self, shaderFile):
        shader = ""
        archivo = open(shaderFile, "r")
        linea = archivo.readline()
        
        while linea:
            # UNE EL CONTENIDO COMPLETO DE LOS ARCHIVOS DE SHADERS
            shader += linea
            linea = archivo.readline()
        archivo.close()

        return shader
