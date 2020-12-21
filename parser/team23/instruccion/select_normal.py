from abstract.instruccion import *
from tools.tabla_tipos import *
from tools.console_text import *

class select_normal(instruccion):
    def __init__(self,distinto,listaO,expresiones,fin, line, column, num_nodo):
        super().__init__(line,column)
        self.distinto=distinto
        self.fin=fin
        self.listaO=listaO
        self.nodo = nodo_AST('SELECT',num_nodo)
        self.nodo.hijos.append(nodo_AST('SELECT',num_nodo+1))
        self.expresiones=expresiones
        
        if (distinto!=None):
            self.nodo.hijos.append(nodo_AST(distinto,num_nodo+2))

        if (listaO=='*'):
            self.nodo.hijos.append(nodo_AST(listaO,num_nodo+3))
        else:
            if listaO != None:
                for element3 in listaO:
                    if element3 != None:
                        self.nodo.hijos.append(element3.nodo)

        self.nodo.hijos.append(nodo_AST('FROM',num_nodo+4))
        print('Si jala select')


        if expresiones != None:
            for element2 in expresiones:
                if element2 != None:
                    self.nodo.hijos.append(element2.nodo)
        
        if fin != None:
            for element in fin:
                if element != None:
                    self.nodo.hijos.append(element.nodo)
        
    def ejecutar(self):
        pass 