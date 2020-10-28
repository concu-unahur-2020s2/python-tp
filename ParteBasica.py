import logging
import threading
import random
import time



logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Heladera:

    def __init__(self,cantLatasMax,cantBotellasMax):
        self.cantLatasMax = cantLatasMax
        self.cantBotellaMax = cantBotellasMax
        self.cantTotalLatas = 0
        self.cantTotalBotellas = 0


    def estaLLena(self):
        return self.cantTotalLatas <= self.cantLatasMax

    def ponerLatas(self, cant):
        if not self.estaLLena():
            print('esta llena')
            self.cantTotalLatas += cant

    def ponerBotellas(self,cant):
        self.cantTotalBotellas += cant

heladera = Heladera(15,10)
heladera.ponerLatas(18)
print(heladera.cantTotalLatas)
print(heladera.estaLLena())

