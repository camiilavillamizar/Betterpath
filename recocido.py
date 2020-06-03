import math,json,time,urllib.parse,urllib.request
from flask import jsonify
from random import sample, randint, uniform
from matrixes import working
key = 'AIzaSyBwogYJ7xQkoQ-lunCXWsobGvLxU9fayIk'
base_url_distance_matrix = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='


global adjacency_matrix_times, adjacency_matrix_distances
adjacency_matrix_times = []
adjacency_matrix_distances = []
#places = {1: [10.424646, -75.5408702], 2: [10.4270046, -75.5453768], 3: [10.4249692, -75.5468839], 4: [10.3932277, -75.4832311]}

#workinghard('driving', {1: [10.424646, -75.5408702], 2: [10.4270046, -75.5453768], 3: [10.4249692, -75.5468839], 4: [10.3932277, -75.4832311]})


####Proceso de recocido simulado

##La siguiente función realiza el proceso de two opt

#realiza el proceso 2opt, cambiando aleatoriamente 2 posiciones
def two_opt(x):
    dx = x[:]
    num1, num2 = 0,0
    while (num1 == num2):
        num1 = randint(1, len(x)-1)
        num2 = randint(1, len(x)-1)
    aux = dx[num1]
    dx[num1] = dx[num2]
    dx[num2] = aux
    return dx #retorna la funcion perturbada

##La siguiente función halla el tiempo total de un recorrido (función objetivo)

#evalua la funcion objetivo (tiempo)
def objective_function(ax):
    global adjacency_matrix_times
    time_traveled = 0
    
    for place in range (len(ax)-1):
        time_traveled += adjacency_matrix_times[ax[place]-1][ax[place+1]-1]
    
    return time_traveled #Retorna el tiempo total aproximado que se gasta en el recorrido


##Esta función halla la distancia total de un recorrido

#evalua la funcion objetivo (distancia)
def objective_function_distance(ax):
    global adjacency_matrix_distances
    distance_traveled = 0
    
    for place in range (len(ax)-1):
        distance_traveled += adjacency_matrix_distances[ax[place]-1][ax[place+1]-1]
    
    return distance_traveled #Retorna la distancia total recorrida


##Esta función devuelve las coordenadas del recorrido de manera ordenada
def coordinates(x,places):
    marks = []
    for i in x:
        mark = []
        for c, v in places.items():
            if (i == c):
                mark = (v[0], v[1])
                marks.append(mark)
    return marks

##Esta función realiza el cambio de x al encontrar una mejor solución y la imprime
#Realiza los cambios cuando x = dx
def sub_process(dx, zdx,x,T):
    global alfa
    x = dx
    T = alfa*T
    return x,T


##Esta función realiza el proceso de boltzman
#evalua la distribucion de probabilidad de boltzman
def boltzman(ax, dx,T):
    delta = objective_function(dx) - objective_function(ax)
    p = math.exp(-delta/T)
    return p

##Esta función realiza el proceso de recocido simulado
#Realiza el proceso de recocido simulado
def sa_process(x,T):
    #se perturba (tecnica opt)
    dx = two_opt(x)
    actualx = x[:]

    zdx = objective_function(dx)
    zx = objective_function(actualx)

    if(zdx < zx):
        x,T = sub_process(dx, zdx,x,T)
    else: 
        n = uniform(0, 1)
        if(n < boltzman(actualx, dx,T)):
            x,T = sub_process(dx, zdx,x,T) 
    return x,T


global Tf, alfa

alfa = 0.9
Tf = 0.1
inicio = 1


##Proceso
def workinghard(option,places,timer, T):
    global alfa,adjacency_matrix_distances,adjacency_matrix_times,Tf
    adjacency_matrix_times,adjacency_matrix_distances=working(option,adjacency_matrix_times,adjacency_matrix_distances,places)
    information = []
    places_index = dict()
    index = []
    i=0
    
    places_names = [i for i in places.keys()]
    for j in range (len(places_names)): 
        places_index[j + 1] = places_names[j]
        index.append(j + 1)

    print(",".join(map(str, index)))
    #se genera una solucion aleatoria 
    x = sample(index, len(index))
    for place in range (len(x)):
        if (inicio == x[place]):
            aux = x[0]
            x[0] = x[place]
            x[place] = aux  

    print("Recorrido: ", x)
    timeout = time.time()+60*timer
    print("T: ", T)
    print("Tf: ", Tf)
    print("alfa: ",alfa)
    print("timer:",timer)
    print("i: ",i)
    while (T > Tf): 
        x,T = sa_process(x,T)
        i += 1
        if time.time()>=timeout:
            print(i,T)
            break
    print(i,T)
    zdx = objective_function(x)
    zdxd = objective_function_distance(x)
    
    print("Recorrido ", x)
    print("Tiempo aproximado: ", zdx, "segundos,", zdx/60, "minutos", (zdx/60)/60, "horas")
    print("Distancia total en metros: ", objective_function_distance(x))


    return(x,zdx,zdxd)
