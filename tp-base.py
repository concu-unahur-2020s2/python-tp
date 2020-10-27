import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

botellasSobrantes = 0
latasSobrantes = 0
heladeras = []
semaforoHeladeras = threading.Semaphore(1)

cantidadHeladeras = 2
cantidadProveedores = 2


def hayHeladerasDisponibles():
    i = 0
    resultado = False
    while i < len(heladeras):
        h = heladeras[i]
        if h.hayEspacio():
            resultado = True
        i += 1
    return resultado

def elegirHeladera():
    global heladeras
    i = 0
    if hayHeladerasDisponibles():
        heladeraConEspacio = None
        try:
            while i < len(heladeras):
                heladeraActual = heladeras[i]
                while heladeraActual.hayEspacio():
                    heladeraConEspacio = heladeraActual
                    raise Exception("Se encontro")
                i += 1
        except:
            return heladeraConEspacio

class Heladera():
    def __init__(self, nombre):
        self.botellas = []
        self.latas = []
        self.nombre = nombre

    def hayEspacio(self):
        if len(self.botellas) == 10 and len(self.latas) == 15:
            return False
        else:
            return True

    def agregarBotella(self, cantidad):
        aPoner = cantidad

        while len(self.botellas) < 10:
            self.botellas.append(1)
            aPoner -= 1
        time.sleep(2)

        if aPoner > 0:
            return aPoner
        else:
            return 0
    
    def agregarLata(self, cantidad):
        aPoner = cantidad
        
        while len(self.latas) < 15:
            self.latas.append(1)
            aPoner -= 1
        time.sleep(2)

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
        botellasAPoner = self.cantAPoner() + botellasSobrantes
        latasAPoner = self.cantAPoner() + latasSobrantes

        logging.info("Agregando " + str(botellasAPoner) + " Botellas en heladera " + str(heladera.nombre))
        sobranteBotellas = heladera.agregarBotella(botellasAPoner)

        logging.info("Agregando " + str(latasAPoner) + " Latas en heladera " + str(heladera.nombre))
        sobranteLatas = heladera.agregarLata(latasAPoner)

        logging.info("Sobraron " + str(sobranteBotellas) + " Botellas y " + str(sobranteLatas) + " latas.")

        botellasSobrantes += sobranteBotellas
        latasSobrantes += sobranteLatas

    def run(self):
        semaforoHeladeras.acquire()

        if hayHeladerasDisponibles():
            self.reponer(elegirHeladera())
        else:
            logging.info("Las heladeras estan llenas!")

        semaforoHeladeras.release()

                
                    
    
          
for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

for i in range(cantidadProveedores):
    nombre = 'Proveedor ' + str(i)
    Proveedor(nombre).start()



