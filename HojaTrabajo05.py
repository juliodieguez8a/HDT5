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

def proceso(env, t_crea, nombre, ram, mem, ins, ins_x_t):

    global tiempoTOTAL #variable con el tiempo TOTAL acumulado de los procesos
    
    #NEW
    # Simular tiempo de llegada de proceso
    yield env.timeout(t_crea)
    print('t: %f - %s (new) solicita -> %d de ram' % (env.now, nombre, mem))

    #Obtener tiempo de llegada
    tiempoLlegada = env.now # aqui llego el proceso
    
    #ADMITTED->READY
    #solicita memoria
    yield ram.get(mem)
    print('t: %f - %s (admited) acepta solicitud por -> %d de ram' % (env.now, nombre, mem))

    
    completado = 0
    
    while completado < ins:

        #READY
        #pedimos conectarnos con cpu
        with cpu.request() as req:
            yield req
            #Determinar instrucciones a realizar
            if (ins-completado)>=3:
                eje=3
            else:
                eje=(ins-completado)

            print('t: %f - %s (ready) cpu ejecutara %d instrucciones' % (env.now, nombre, eje))
            #El tiempo de ejecucion es de 1/(instrucciones por unidad de tiempo) con "eje" instrucciones a realizar 
            yield env.timeout(eje/ins_x_t)

            #Actualizar instrucciones completadas
            completado += eje
            print('t: %f - %s (runing) cpu -> (%d/%d) completado' % (env.now, nombre, completado, ins))

        #despacho: Numero aleatorio (1 para espera en cola, 2 directo a ready)
        despacho = random.randint(1,2)

        #si la opcion en despacho es 1 y no ha terminado va a cola waiting
        if despacho == 1 and completado<ins:
            #WAITING
            with waiting.request() as req2:
                yield req2
                #suponemos espera de 1 unidad de tiempo en cola de operaciones i/o
                yield env.timeout(1)                
                print('t: %f - %s (waiting) realizadas operaciones (i/o)' % (env.now, nombre))

        #si la opcion en despacho es 2 y no ha terminado regresara a ready

    

    #EXIT->TERMINATED
    #devuelve memoria
    yield ram.put(mem)
    print('t: %f - %s (terminated) finaliza, retorna -> %d de ram' % (env.now, nombre, mem))

    #Actualizar tiempo Total
    # Se agraga al tiempo total el tiempo de este proceso (tiempo actual - tiempo de llegada)
    tiempoTOTAL += (env.now - tiempoLlegada)  



memoria_ram=100 #100 unidades de memoria ram
ins_x_t = 3.0 #ejecuta 3 instrucciones por unidad de tiempo
tiempoTOTAL = 0.0 #tiempo de todos los procesos
n_procesos = 25 # numero de procesos a ejecutar


env = simpy.Environment()  #crear ambiente de simulacion
ram = simpy.Container(env, init=memoria_ram, capacity=memoria_ram) #el cargador de bateria soporta 2 carros
cpu = simpy.Resource (env, capacity=1) #cola para acceso a cpu
waiting = simpy.Resource (env, capacity=1) #cola para acceso a operaciones i/o

# Crear Semilla para random
random.seed(1234)

interval = 10 #cada 10


# crear los procesos
for i in range(n_procesos):
    t_crea = random.expovariate(1.0 / interval)
    ins = random.randint(1,10) #Cantidad de instrucciones
    mem = random.randint(1,10) #Cantidad de memoria a solicitar
    env.process(proceso(env, t_crea, 'Proceso %d' % i, ram, mem, ins, ins_x_t))

# correr la simulacion
env.run()
print "El PROMEDIO de tiempo por proceso es ", tiempoTOTAL / n_procesos
print "fin"

