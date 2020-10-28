import logging
import threading
import random
import time



logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Heladera:

    def __init__(self,nombre,cantLatasMax,cantBotellasMax):
        self.cantLatasMax = cantLatasMax
        self.cantBotellaMax = cantBotellasMax
        self.nombre = nombre

    def ponerLatas(self, cant):
        total = 0
        while self.cantLatasMax < cant:
            total += cant


heladera = Heladera()
heladera.ponerLatas(2)
print(heladera.cantLatasMax)

