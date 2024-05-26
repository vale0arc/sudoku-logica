from itertools import combinations
from Logica import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from types import MethodType

def escribir_rejilla(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    n, x, y  = self.unravel(atomo)
    return f"El número {n}{neg} está en la casilla ({x},{y})"
     
class Rejilla:

    '''
    Clase para representar el problema de poner
    un número distinto en cada una de las casillas
    de una rejilla nxn
    '''

    def __init__(self):
        self.N = 4
        self.M = 4
        self.NenC = Descriptor([self.N * self.M, self.N, self.M])
        self.NenC.escribir = MethodType(escribir_rejilla, self.NenC)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        r4 = self.regla4()
        self.reglas = [r1,r2,r3,r4]
        
    def regla1(self):
        casillas = [(x,y) for n in range (16) for x in range(4) for y in range(4)]
        lista = []
        for c in casillas:
            x,y = c
            otros_num = [n for n in range(4)]
            lista_o = []
            for p in otros_num:
                lista_o.append(self.NenC.ravel([p,x,y]))
            form = Otoria(lista_o) 
            lista.append(form)
        return Ytoria(lista)

    def regla2(self):
        casillas_num = [(n,x,y) for x in range(4) for y in range(4) for n in range(4)]
        lista = []
        for c in casillas_num:
            n,x,y = c
            otras_cas = self.region(n,x,y)
            lista_o = []
            for m in otras_cas:
                lista_o.append(self.NenC.ravel([*m]))
            form = '(' + self.NenC.ravel([*c]) + '>-' + Otoria(lista_o) + ')'
            lista.append(form)
        return Ytoria(lista)
    
    def region(self, n,x,y):
        otras_casillas = []
        if (x==0 or x==1) and (y==0 or y==1):
            otras_casillas=[(n,x1,y1) for y1 in range(2)  for x1 in range(2) if x1!= x or y1!=y]
        if (x==0 or x==1) and (y==2 or y==3):
            otras_casillas=[(n,x1,y1) for y1 in range(2,4) for x1 in range(2) if x1!= x or y1!=y]
        if (x==2 or x==3) and (y==0 or y==1):
            otras_casillas=[(n,x1,y1) for y1 in range(2) for x1 in range(2,4) if x1!= x or y1!=y]
        if (x==2 or x==3) and (y==2 or y==3):
            otras_casillas=[(n,x1,y1) for y1 in range(2,4) for x1 in range(2,4) if x1!= x or y1!=y]
            
        return otras_casillas
        

    def regla3(self):
        casillas_num = [(n,x,y) for n in range(4) for x in range(self.N) for y in range(self.M)]
        lista = []
        for c in casillas_num:
            n,x,y = c
            otras_columnas = [y1 for y1 in range(4) if y1 != y]
            lista_o = []
            for p in otras_columnas:
                lista_o.append(self.NenC.ravel([n,x,p]))
            form = '(' + self.NenC.ravel([*c]) + '>-' + Otoria(lista_o) + ')'
            lista.append(form)
        return Ytoria(lista)

    def regla4(self):
        casillas_num = [(n, x, y) for n in range(4) for x in range(self.N) for y in range(self.M)]
        lista = []
        for c in casillas_num:
            n, x, y = c
            otras_filas = [x1 for x1 in range(4) if x1 != x]
            lista_o = []
            for l in otras_filas:
                lista_o.append(self.NenC.ravel([n, l, y]))
            form = '(' + self.NenC.ravel([*c]) + '>-' + Otoria(lista_o) + ')'
            lista.append(form)
        return Ytoria(lista)

    def visualizar(self, I):
        fig, axes = plt.subplots()
        fig.set_size_inches(self.N, self.M)
        step_x = 1. / self.N
        step_y = 1. / self.M
        offset = 0.001
        tangulos = []
        tangulos.append(patches.Rectangle((0, 0), 1, 1, \
        facecolor = 'cornsilk', edgecolor = 'black', linewidth = 2))
        u = self.N // 2 if self.N % 2 == 0 else self.N // 2 + 1 # Filas par o impar
        v = self.M // 2 if self.M % 2 == 0 else self.M // 2 + 1 # Columnas par o impar
        for i in range(u + 1):
            for j in range(v):
                tangulos.append(patches.Rectangle((2 * i * step_x, 2 * j * step_y), \
                                                  step_x - offset, step_y, \
                                                  facecolor = 'lightslategrey', \
                                                  ec = 'k', lw = 3))
                tangulos.append(patches.Rectangle((step_x + 2 * i * step_x, (2 * j + 1) * step_y), \
                                                  step_x - offset, step_y, \
                                                  facecolor = 'lightslategrey', \
                                                  ec = 'k', lw = 3))
        for t in tangulos:
            axes.add_patch(t)
        offsetX = 0.065
        offsetY = 0.065
        for k in I:
            n, X, Y = self.NenC.unravel(k)
            if I[k]:
                axes.text(X * step_x + step_x / 2, Y * step_y + step_y / 2, n, \
                          ha = "center", va = "center", size = 30, c = 'k')
        axes.axis('off')
        plt.show
