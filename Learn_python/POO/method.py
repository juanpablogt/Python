#Clase para explicar el concepto de classmethod.
class Pastel:
    def __init__(self,ingredientes):
        self.ingredientes = ingredientes

    def __repr__(self):
        return f'Ingredientes({self.ingredientes !r})'

#Es mas dependiente del la clase a diferencia del static
    @classmethod
    def Pastel_chocolate(cls):
        return cls (['harina,huevos,chocolate'])
    @classmethod
    def Pastel_vainilla(cls):
        return cls(['harina,huevos,vainilla'])
        
print(Pastel.Pastel_chocolate())