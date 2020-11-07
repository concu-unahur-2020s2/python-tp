import logging

import random
import threading
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)

latasSobrantes = 0
botellasSobrantes = 0
latasEntregadas = 10
botellasEntregadas = 0
heladeras = []
cantHeladeras = 2
cantProvedores = 4

semaforoHeladera = threading.Semaphore()


class Heladera:
    def __init__(self, numero):
        self.numero = f'heladera numero {numero}'
        self.capMaximaLatas = 15  # capacidad maxima de latas
        self.capMaximaBotellas = 10  # capacidad maxima de botellas
        self.totalLatas = 0  # total de latas cargadas
        self.totalBotellas = 0  # total botallas cargadas
        self.estado = False  # indica si la heladera esta prendia

    def estaLlena(self):  # si la heladera tiene toda su capacidoad maxima cargada
        return not self.tieneLugarLatas() and not self.tieneLugarBotellas()

    def tieneLugarLatas(self):
        return self.totalLatas < self.capMaximaLatas

    def tieneLugarBotellas(self):

        return self.totalBotellas < self.capMaximaBotellas

    def cargarLata(self):

        if self.totalLatas < self.capMaximaLatas:
            self.totalLatas += 1
            logging.info(f'ser cargo un lata en la heladera {self.numero}')
            logging.info(f'total de latas cargadas en la heladera -> {self.totalLatas}')

    def cargarBotellas(self):

        if self.totalBotellas < self.capMaximaBotellas:
            self.totalBotellas += 1
            logging.info(f'ser cargo un botellas en la heladera {self.numero}')
            logging.info(f'total de botellas cargadas en la heladera -> {self.totalBotellas}')

    def enchufarHeladera(self):

        self.estado = True
        logging.info(f'prendiendo la heladera {self.numero}')
        time.sleep(2)


class Proveedor(threading.Thread):

    def __init__(self, nombre):

        super().__init__()
        self.name = nombre
        self.cantAEntregarLatas = random.randint(0, 15)
        self.cantAEntragarBotellas = random.randint(0, 10)

    def reponerLatas(self, heladera):
        global latasSobrantes, latasEntregadas
        latasSobrantes += self.cantAEntregarLatas
        logging.info(f'lastas en stock {self.cantAEntregarLatas}')

        while latasSobrantes > 0:
            if heladera.tieneLugarLatas():
                heladera.cargarLata()
                latasSobrantes -= 1
        logging.info(f'total de latas en heladera {heladera.totalLatas}')
        logging.info(f'sobraron {latasSobrantes} latas')

    def reponerBotellas(self, heladera):
        global botellasSobrantes, botellasEntregadas
        botellasSobrantes += self.cantAEntragarBotellas
        logging.info(f'botellas en stock {self.cantAEntragarBotellas}')

        while botellasSobrantes > 0:
            if heladera.tieneLugarBotellas():
                heladera.cargarBotellas()
                botellasSobrantes -= 1
        logging.info(f'total de latas en heladera {heladera.totalBotellas}')
        logging.info(f'sobraron {botellasSobrantes} botellas')
        time.sleep(random.randint(1, 2))

    def run(self):

        semaforoHeladera.acquire()
        for i in heladeras:
            self.reponerLatas(i)
            self.reponerBotellas(i)
        semaforoHeladera.release()


for h in range(cantHeladeras):
    heladeras.append(Heladera(h))

for p in range(cantProvedores):
    Proveedor(p).start()
