import math
class pastel:
    def __init__(self,ingredientes,tamanio):
        self.ingredientes=ingredientes
        self.tamanio=tamanio
    
    def __repr__(self):
        return (f'Ingredientes({self.ingredientes}, 'f'{self.tamanio})')

    def area(self):
        return tamanio_area(self.tamanio)
    
    #Es algo mas independiente de la clase
    @staticmethod
    def tamanio_area(A):
        return A**2*math.pi

pastel1 = pastel(['harina,huevos'],4)
print(pastel1.area())