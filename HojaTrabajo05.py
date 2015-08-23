import simpy
import random

#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# name: identificacion del carro
# bcs:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria

def proceso(env, ram):
    global tiempoTOTAL
    ram.
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))

    tiempoLlegada = env.now # aqui llego el carro
    with ram.request() as req:  #pedimos conectarnos al cargador de bateria
        yield req

        # Charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del cargador bcs
    tiempoTotalxCarro = env.now - tiempoLlegada
    tiempoTOTAL = tiempoTOTAL + tiempoTotalxCarro #usar aqui una lista [ ]
    
#
env = simpy.Environment()  #crear ambiente de simulacion
ram = simpy.Container(env, capacity=100) #el cargador de bateria soporta 2 carros
                                      #a la vez
tiempoTOTAL = 0.0 #tiempo de todos los carros
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
interval = 5 # cada 10 segundos ...

# crear los carros
for i in range(25):
    t = random.expovariate(1.0 / interval)
    tcarga = random.randint(1,5)
    env.process(car(env, 'Car %d' % i, bcs, t, tcarga))

# correr la simulacion
env.run()
print "el promedio es ", tiempoTOTAL / 25
