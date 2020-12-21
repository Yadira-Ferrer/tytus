import math
from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato, Tipo
from Instrucciones.Excepcion import Excepcion

class PI(Instruccion):
    def __init__(self, linea, columna):
        Instruccion.__init__(self,Tipo(Tipo_Dato.DOUBLE_PRECISION),linea,columna)

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        return math.pi
