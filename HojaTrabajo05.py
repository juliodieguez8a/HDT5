# -*- coding: cp1252 -*-

#UVG – Algoritmos y Estructura de Datos, Seccion 10
#Pedro Joaquin Castillo Coronado 14224
#Julio Ronaldo Dieguez Ochoa Carne 14475

import simpy
import random



def proceso(env, t_crea, nombre, ram, mem, ins, ins_x_t):
    global lista
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
            if (ins-completado)>=ins_x_t:
                eje=ins_x_t
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
    lista.append(env.now - tiempoLlegada)
    tiempoTOTAL += (env.now - tiempoLlegada)  


lista=[] #lista en la que se guardan los tiempos de cada proceso
memoria_ram= 100 #100 unidades de memoria ram
ins_x_t = 3.0 #ejecuta 3 instrucciones por unidad de tiempo
tiempoTOTAL = 0.0 #tiempo de todos los procesos
n_procesos = 100 # numero de procesos a ejecutar


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
promedio =(tiempoTOTAL / n_procesos)
print "El PROMEDIO de tiempo por proceso es ", promedio

#Calculo de desviacion standar
temp=0
for i in lista:
    temp+=(i-promedio)**2

des=(temp/n_procesos)**0.5
print "La desviacion estandar es: ", des
print "fin"
