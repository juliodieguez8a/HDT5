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

def proceso(env, t_crea, nombre, ram, mem, ins):

    # Simular tiempo de llegada de proceso
    yield env.timeout(t_crea)

    # Request one of its charging spots
    print('t: %d - %s solicita -> %d de ram' % (env.now, nombre, mem))

    #solicita memoria
    yield ram.get(mem)
    
    print('t: %d - %s acepta solicitud por -> %d de ram' % (env.now, nombre, mem))

    yield env.timeout(25)

    #devuelve memoria
    yield ram.put(mem)
    print('t: %d - %s finaliza, retorna -> %d de ram' % (env.now, nombre, mem))

env = simpy.Environment()  #crear ambiente de simulacion
ram = simpy.Container(env, init=100, capacity=100) #el cargador de bateria soporta 2 carros
cpu = simpy.Resource (env, capacity=1)
                                      #a la vez
# Crear Semilla para random
random.seed(1234)

interval = 10 #cada 10
# crear los procesos
for i in range(25):
    t_crea = random.expovariate(1.0 / interval)
    ins = random.randint(1,10) #Cantidad de instrucciones
    mem = random.randint(1,10) #Cantidad de memoria a solicitar
    env.process(proceso(env, t_crea, 'Proceso %d' % i, ram, mem, ins))

# correr la simulacion
env.run()
print "fin"
