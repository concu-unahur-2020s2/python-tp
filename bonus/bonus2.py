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
monitorBeode = threading.Condition()

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
        logging.info("Iniciando enfriado rapido en heladera "+ str(heladeras[heladeraConEspacio].nombre))
        heladeraConEspacio += 1
        if heladeraConEspacio == len(heladeras):
            heladeraConEspacio = 0
        else:
            logging.info("Enchufando heladera "+ str(heladeras[heladeraConEspacio].nombre)+ "\n")

def lataPinchada():
    global heladeras
    indiceRandom = random.randint(0,len(heladeras)-1)
    h = heladeras[indiceRandom]
    caso = random.choice([0,1,2,3,4])
    if caso == 3:
        h.latas.pop(0)
        print("Se ha pinchado una lata \n")


        


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
    
    def hayBotellas(self):
        return len(self.botellas) > 0
    
    def hayLatas(self):
        return len(self.latas) > 0

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
        lataPinchada()
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
            with monitorBeode:
                self.reponer(heladeras[heladeraConEspacio])
                monitorBeode.notify()
        else:
            logging.info("Las heladeras estan llenas!")
        
        semaforoHeladeras.release()

class Beode(threading.Thread):
    def __init__(self,monitor, nombre, limite,tipoDeConsumo):
        super().__init__()
        self.name = nombre
        self.limite = limite
        self.consumo = 0
        self.tipoDeConsumo = tipoDeConsumo
        self.monitor = monitor
    
    def elegirHeladera(self):
        h = random.randint(0,len(heladeras)-1)
        return heladeras[h]
    
    def consumirBotella(self, heladera):
        semaforoHeladeras.acquire()
        if heladera.hayBotellas():
            heladera.botellas.pop(0)
            self.consumo += 1
            logging.info("Estoy bebiendo "+ self.tipoDeConsumo + " de la heladera " + str(heladera.nombre) + " voy tomando "+ str(self.consumo) + "\n")
            semaforoHeladeras.release()
        else:
            semaforoHeladeras.release()
            logging.info("No hay lo que quiero tomar en la heladera " + str(heladera.nombre) + "\n")
            self.monitor.wait()
    
    def consumirLata(self, heladera):
        semaforoHeladeras.acquire()
        if heladera.hayLatas():
            heladera.latas.pop(0)
            self.consumo += 1
            logging.info("Estoy bebiendo "+ self.tipoDeConsumo + " de la heladera " + str(heladera.nombre) + " voy tomando "+ str(self.consumo) + "\n")
            semaforoHeladeras.release()
        else:
            semaforoHeladeras.release()
            logging.info("No hay lo que quiero tomar en la heladera " + str(heladera.nombre) + "\n")
            self.monitor.wait()

    def consumir(self,heladera):
        if self.tipoDeConsumo.lower() == "botella":
            self.consumirBotella(heladera)
        elif self.tipoDeConsumo.lower() == "lata":
            self.consumirLata(heladera)
        elif self.tipoDeConsumo.lower() == "ambos":
            alAzar = random.choice([0,1])
            if alAzar == 0:
                self.consumirBotella(heladera)
            if alAzar == 1:
                self.consumirLata(heladera)
        time.sleep(3)

    def run(self):
        while self.consumo < self.limite:
            with self.monitor:
                self.consumir(self.elegirHeladera())
        logging.info("Me canse de tomar me voy a dormir")
                
             

            
for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))
time.sleep(5)

for i in range(cantidadProveedores):
    nombre = 'Proveedor ' + str(i)
    Proveedor(nombre).start()

bb = Beode(monitorBeode,"Pepe",5,"botella")  
bb.start()  

bl= Beode(monitorBeode, "Eduardo", 2, "lata")
bl.start()

ba= Beode(monitorBeode,"Barbi", 5, "ambos")
ba.start()




