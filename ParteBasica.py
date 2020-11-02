import logging
import threading
import random
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)
latasSobrantes = 0
botellasSobrantes = 0
cantLatas = 10
cantBotellas = 4
semaforoHeladera = threading.Semaphore()


class Heladera(threading.Thread):

    def __init__(self, cantLatasMax, cantBotellasMax):
        super().__init__()
        self.cantLatasMax = cantLatasMax
        self.cantBotellaMax = cantBotellasMax
        self.cantTotalLatas = 0
        self.cantTotalBotellas = 0

    def cantidadEspacioDiponible(self):
        return self.cantLatasMax - self.cantTotalLatas

    def ponerLata(self):
        self.cantTotalLatas += 1

    def ponerBotella(self):
        self.cantTotalBotellas += 1

    def llenarHeladeraConLatas(self, cant):
        cantAPoner = cant
        global latasSobrantes
        latasSobrantes = cantAPoner - self.cantTotalLatas
        while cantAPoner > 0:
            if self.cantidadEspacioDiponible() > 0:
                self.ponerLata()
            cantAPoner -= 1
            logging.info("poniendo una lata")
            time.sleep(random.randint(1, 2))

    def llenarHeladeraConBotellas(self, cant):
        cantAPoner = cant
        global botellasSobrantes
        botellasSobrantes = cantAPoner - self.cantTotalBotellas
        while cantAPoner > 0:
            if self.cantidadEspacioDiponible() > 0:
                self.ponerBotella()
            cantAPoner -= 1
            logging.info("poniendo botellas")
            time.sleep(random.randint(1, 2))

    def run(self):
        semaforoHeladera.acquire()

        self.llenarHeladeraConBotellas(15)
        self.llenarHeladeraConLatas(10)


class Proveedor(threading.Thread):

    def __int__(self, nombre):
        super().__init__()
        self.nombre = nombre

    # def run(self):


heladera = Heladera(15, 10)
heladera.start()
