class telefono:
    def __init__(self):
        pass
    def encender(self):
        print("El telefono esta encendido")

class camara:
    def __init__(self):
        pass
    def photo(self):
        print("Tomando photo")
    def video(self):
        print("El telefono esta tomando video")

class linea:
    def __init__(self):
        pass
    def llamada(self):
        print("Llamando...")
    def colgar(self):
        print("Colgado...")

class iphone(telefono,camara,linea):
        def __del__(self):
            print("El telefono ha finalizado la accion")


cel1 = iphone()
print(cel1.colgar())