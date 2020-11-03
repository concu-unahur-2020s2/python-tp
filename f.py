import random
import logging
import threading
import time

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantidadMaximaLatas = 10
cantidadMaximaBotellas = 15
# CUANDO SE ENTREGA LA MERCADERIA POR EL PROVEEDOR SE GUARDA EN LA DESPENSA
latasEnDespensa = []
botellasEnDespensa = []
cantHeladeras = 5
cantProveedores = 40
listaHeladeras = []
# SEMAFORO PARA CARGA DE HELADERA
semaforocargaHeladera = threading.Semaphore(1)




class Proveedor(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.nombre = nombre
        self.latasAEntregar = random.randint(1, 5)
        self.botellasAEntregar = random.randint(1, 5)

    def decargarLatas(self):
        logging.info(
            f'Proveeror {self.numero}: Le entrego {self.latasAEntregar} latas')
        for i in range(self.latasAEntregar):
            latasEnDespensa.append(1)

    def descargarBotellas(self):
        logging.info(
            f'Proveeror {self.numero}: Le entrego {self.botellasAEntregar} botellas')
        for i in range(self.latasAEntregar):
            botellasEnDespensa.append(1)

    def run(self):
        self.decargarLatas()
        self.descargarBotellas()



for i in range(cantProveedores):
    Proveedor(i).start()