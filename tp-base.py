import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

botellasSobrantes = 0
latasSobrantes = 0
heladeras = []
heladeraConEspacio = 0
semaforoHeladeras = threading.Semaphore(1)

cantidadHeladeras = 5
cantidadProveedores = 20


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
    global heladeras, heladeraConEspacio
    if not heladeras[heladeraConEspacio].hayEspacio():
        print("Iniciando enfriado rapido en heladera", heladeras[heladeraConEspacio].nombre)
        heladeraConEspacio += 1
        print("Enchufando heladera", heladeras[heladeraConEspacio].nombre, "\n")

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
        try:
            while aPoner > 0:
                if len(self.botellas) == 10:
                    raise Exception("La heladera se lleno de botellas")
                self.botellas.append(1)
                aPoner -= 1
        except:
            pass
        time.sleep(random.randint(3, 10))

        if aPoner > 0:
            return aPoner
        else:
            return 0
    
    def agregarLata(self, cantidad):
        aPoner = cantidad
        
        try:
            while aPoner > 0:
                if len(self.latas) == 15:
                    raise Exception("La heladera se lleno de latas")
                self.latas.append(1)
                aPoner -= 1
        except:
            pass
        time.sleep(random.randint(3, 10))

        if aPoner > 0:
            return aPoner
        else:
            return 0
    
    def estadoActual(self):
        return "La heladera "+ str(self.nombre) +" tiene " + str(len(self.botellas)) + " Botellas y "+ str(len(self.latas)) + " Latas"


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

        logging.info("Ingreso " + str(botellasAPoner) + " Botellas y " + str(latasAPoner) + " Latas")
        
        sobranteBotellas = heladera.agregarBotella(botellasAPoner)
        sobranteLatas = heladera.agregarLata(latasAPoner)

        logging.info(heladera.estadoActual())
        logging.info("Sobraron " + str(sobranteBotellas) + " Botellas y " + str(sobranteLatas) + " latas.\n")

        botellasSobrantes += sobranteBotellas
        latasSobrantes += sobranteLatas

    def run(self):
        global heladeraConEspacio
        semaforoHeladeras.acquire()

        if hayHeladerasDisponibles():
            elegirHeladera()
            self.reponer(heladeras[heladeraConEspacio])
        else:
            logging.info("Las heladeras estan llenas!")
        
        semaforoHeladeras.release()

                
    
for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

for i in range(cantidadProveedores):
    nombre = 'Proveedor ' + str(i)
    Proveedor(nombre).start()



