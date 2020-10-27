import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

botellasSobrantes = []
latasSobrantes = []
heladeras = []
semaforoHeladeras = threading.Semaphore(0)

cantidadHeladeras = 1
cantidadProveedores = 1

class Heladera():
    def __init__(self, nombre):
        self.botellas = []
        self.latas = []
        self.nombre = nombre

    def enchufar(self):
        print("Enchufando heladera..")
        time.sleep(2)

    def enfriamientoRapido(self):
        print("Iniciando el enfriamiento rapido")
        time.sleep(1)

    def hayEspacio(self):
        if len(self.botellas) == 10 and len(self.latas) == 15:
            return False
        else:
            return True

    def agregarBotella(self, cantidad):
        aPoner = cantidad
        print("Agregando " + str(cantidad) + " Botellas en heladera " + str(self.nombre))
        while len(self.botellas) < 10:
            self.botellas.append(1)
            aPoner -= 1
            time.sleep(1)
        if aPoner > 0:
            return aPoner
        else:
            return 0
    
    def agregarLata(self, cantidad):
        aPoner = cantidad
        print("Agregando " + str(cantidad) + " Latas en heladera " + str(self.nombre))
        while len(self.latas) < 15:
            self.latas.append(1)
            aPoner -= 1
            time.sleep(1)
        if aPoner > 0:
            return aPoner
        else:
            return 0


class Proveedor(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.name = nombre

    def cantAPoner(self):
        return random.randint(1,10)
                

    def reponer(self, heladera):
        global botellasSobrantes, latasSobrantes

        sobranteBotellas = heladera.agregarBotella(self.cantAPoner())
        sobranteLatas = heladera.agregarLata(self.cantAPoner())

        while sobranteBotellas > 0:
            botellasSobrantes.append(1)
            sobranteBotellas -= 1
        while sobranteLatas > 0:
            latasSobrantes.append(1)
            latasSobrantes -= 1

    def run(self):
        while True:
            
            self.reponer(elegirHeladera)
            time.sleep(5)
            
def hayHeladerasDisponibles():
    i = 0
    resultado = False
    while i < len(heladeras):
        h = heladeras[i]
        if h.hayEspacio:
            resultado = True
        else:
            pass
    return resultado

def elegirHeladera():
    global heladeras
    i = 0

    if hayHeladerasDisponibles():
        heladeraConEspacio = None
        try:
            while i < len(heladeras):
                heladeraActual = heladeras[i]
                if heladeraActual.hayEspacio:
                    heladeraConEspacio = heladeraActual
                    raise Exception("Se encontro")
                i += 1
        except:
            return heladeraConEspacio
    
          
for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

for i in range(cantidadProveedores):
    Proveedor(i).start()



