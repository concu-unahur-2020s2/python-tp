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
cantHeladeras = random.randint(1, 3)
cantProvedores = random.randint(1, 5)

semaforoHeladera = threading.Semaphore()
monitorBeode = threading.Condition()


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


class Beode(threading.Thread):
    def __init__(self, nombre, limite, tipoCerveza, monitor):
        super().__init__()
        self.nombre = nombre
        self.limite = limite
        self.cantidadConsumida = 0
        self.tipo = tipoCerveza
        self.monitor = monitor

    def tomarLata(self, heladera):
        if heladera.tieneLugarLatas():
            heladera.totalLatas -= 1
            self.cantidadConsumida += 1
            logging.info(f'toma lata de la  heladera {heladera.numero}')
        else:
            logging.info(f'no hay lo que quiero tomar de la heladera {heladera.numero}')
            self.monitor.wait()

    def tomarBotella(self, heladera):
        if heladera.tieneLugarBotellas():
            heladera.totalBotellas -= 1
            self.cantidadConsumida += 1
            logging.info(f'me voy a tomar una botella...')
            time.sleep(random.randint(1, 3))
        else:
            logging.info(f'no hay lo que quiero en la heladera {heladera.numero}')
            self.monitor.wait()

    def consumir(self, heladera):
        if self.tipo == 1:
            self.tomarLata()
            time.sleep(2)
            logging.info('tomo latas')
        elif self.tipo.lower() == 2:
            self.tomarBotella()
            time.sleep(2)
            logging.info('tomo botellas')
        elif self.tipo == 3:
            self.tomarLata()
            self.tomarBotella()
            time.sleep(4)
            logging.ifo(f'tomo lata y botellas...')

    def run(self):
        while self.cantidadConsumida < self.limite:
            with self.monitor:
                numero = random.randint(0, len(heladeras) - 1)
                self.tomarLata(heladeras[numero])
        logging.info('me pase de copas... veo doble...')


for h in range(cantHeladeras):
    heladeras.append(Heladera(h))

beode1 = Beode('1', 10, 1, monitorBeode)
beode2 = Beode('1', 15, 2, monitorBeode)
beode3 = Beode('3', 25, 3, monitorBeode)
beode1.start()
beode2.start()
beode3.start()

for p in range(cantProvedores):
    Proveedor(p).start()
