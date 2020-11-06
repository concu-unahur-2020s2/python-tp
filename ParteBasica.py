import logging
import threading
import random
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)
latasSobrantes = 0
botellasSobrantes = 0
cantLatas = 0
cantBotellas = 0
listaHeladeras = []

semaforoHeladera = threading.Semaphore()


class Heladera(threading.Thread):

    def __init__(self,numero):
        super().__init__()

        self.cantLatasMax = 15
        self.cantBotellaMax = 10
        self.cantTotalLatas = 0
        self.cantTotalBotellas = 0
        self.name = f'Heladera{numero}'

    def cantidadEspacioDiponibleLatas(self):
        return self.cantLatasMax - self.cantTotalLatas

    def cantidadEspacioDiponibleBotellas(self):
        return self.cantBotellaMax - self.cantTotalBotellas

    def ponerLata(self):
        self.cantTotalLatas += 1

    def ponerBotella(self):
        self.cantTotalBotellas += 1

    def llenarHeladeraConLatas(self):

        global latasSobrantes, cantLatas
        latasSobrantes = cantLatas - self.cantTotalLatas
        while cantLatas > 0:
            if self.cantidadEspacioDiponibleLatas() > 0:
                self.ponerLata()
            cantLatas -= 1
        logging.info("poniendo  lata...")
        time.sleep(random.randint(1, 2))

    def llenarHeladeraConBotellas(self):

        global botellasSobrantes, cantBotellas
        botellasSobrantes = cantBotellas - self.cantTotalBotellas
        while cantBotellas > 0:
            if self.cantidadEspacioDiponibleBotellas() > 0:
                self.ponerBotella()
            cantBotellas -= 1
        logging.info("poniendo botellas")
        time.sleep(random.randint(1, 2))

    def llenarTodaLaHeladera(self):

        while not self.estaLLena():
            self.llenarHeladeraConBotellas()
            self.llenarHeladeraConLatas()
        logging.info('heladera llena...')

    def run(self):
        semaforoHeladera.acquire()
        while not self.estaLLena():
            self.llenarTodaLaHeladera()
            logging.info(f'cantidad de latas en heladera {self.cantTotalLatas}')
            logging.info(f'cantidad de botellas en la heladera {self.cantTotalBotellas}')
            semaforoHeladera.release()
        logging.info(f'cantidad de latas sobrantes {latasSobrantes}')
        logging.info(f' cantidad de botellas  sobrantes {botellasSobrantes}')

    def estaLLena(self):
        return self.cantTotalBotellas == self.cantBotellaMax and self.cantTotalLatas == self.cantLatasMax


class Proveedor(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.nombre = f'Proovedor {numero}'
        self.latasAEntregar = random.randint(1, 15)
        self.botellasAEntregar = random.randint(1, 10)


    def decargarLatas(self):

        for i in range(self.latasAEntregar):
            global cantLatas
            cantLatas += 1
        logging.info(f'Proveeror: {self.nombre} Le entrego {self.latasAEntregar} total de  latas')
        time.sleep(random.randint(1, 2))

    def descargarBotellas(self):

        for i in range(self.botellasAEntregar):
            global cantBotellas
            cantBotellas += 1
        logging.info(f'Proveeror: {self.nombre} Le entrego {self.botellasAEntregar} total de botellas')
        time.sleep((random.randint(1, 2)))

    def run(self):
        while True:
            self.decargarLatas()
            self.descargarBotellas()
            logging.info(f'latas sobrantes : {latasSobrantes} '
                         f'botellas sobrantes : {cantBotellas}')


cantHeladeras = 2
cantProovedores = 4

for h in range(cantHeladeras):
    Heladera(h).start()

for p in range(cantProovedores):
    Proveedor(p).start()
