class persona:
    def __init__(self,nombre,apellido, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
    
    #Este metodo se llama automaticamente si deseo otro lo llamo con . y el nombre del metodo
    def __str__(self):
        return f"Hi, I'm {self.nombre} {self.apellido} and I'm {self.edad} years old, thanks and bye..."


per1 = persona('Juan Pablo','Gonzalez',33)

print(per1)