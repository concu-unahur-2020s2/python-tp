import logging
import threading
import random
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)

semaforoHeladera = threading.Semaphore()

class Heladera:

    def __init__(self, cantLatasMax, cantBotellasMax):
        self.cantLatasMax = cantLatasMax
        self.cantBotellaMax = cantBotellasMax
        self.cantTotalLatas = 0
        self.cantTotalBotellas = 0

    def hayLugarLatas(self):
        return self.cantTotalLatas <= self.cantLatasMax

    def ponerLata(self):
        self.cantTotalLatas += 1

    def ponerBotella(self, cant):
        self.cantTotalBotellas += 1

    def llenarHeladeraConLatas(self, cant):
        cantAPoner = cant
        sobrante = self.cantLatasMax - cant


        while self.cantTotalLatas <= self.cantLatasMax:
        #while cantAPoner > 0 :
            if self.hayLugarLatas():
                self.ponerLata()

            else:
                raise Exception('no hay mas lugar en la heladera....')
            cantAPoner -= 1




class Proveedor(threading.Thread):

    def __int__(self, nombre):
        super().__init__()
        self.nombre = nombre


    #def run(self):





heladera = Heladera(15, 10)
print(heladera.cantTotalLatas)
heladera.llenarHeladeraConLatas(18)
print(heladera.hayLugarLatas())
print(heladera.cantTotalLatas)
