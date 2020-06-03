import json,urllib.parse,urllib.request, requests
from flask import jsonify

key = 'AIzaSyBwogYJ7xQkoQ-lunCXWsobGvLxU9fayIk'
base_url_distance_matrix = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='


#Se hallan matrices de adyacencia tanto de tiempo (tomando en cuenta el trafico actual)como de distancia.
def working(option,adjacency_matrix_times,adjacency_matrix_distances,places):
    #global places
    directions = len(places.items())
    #print(places)
    #print(len(places.items()))

    # El usuario selecciona como se va a desplazar
    transport = option
    '''
    driving 
    walking 
    bicycling --no funciona 
    '''
    # Se recorre el diccionario
    for c1, v1 in places.items():
        destinations = ''  # Siempre que inicia, inician nuevos destinos
        row_times = []  # Se vacía la lista de tiempos
        row_distances = []  # Se vacía la lista de distancias
        # Se define el orígen
        origin = str(v1[0])+','+str(v1[1])

        # Se recorre nuevamente el diccionario para agregar todos los destinos
        for c2, v2 in places.items():
            # Se agrega cada uno de los destinos
            destinations += str(v2[0])+','+str(v2[1])

            # Si no es el destino final, se agraga | para separar las coordenadas de los destinos
            if (c2 != directions + 1):
                destinations += '|'

        url_distance_matrix = base_url_distance_matrix + origin + '&destinations=' + destinations + '&mode=' + transport + '&key=' + key

        #print(url_distance_matrix)

        response = str(urllib.request.urlopen(url_distance_matrix).read())
        r = requests.get(url_distance_matrix)
        result = r.json()

        if result['status'] == 'OK':
            if (result['rows'][0]['elements'][0]['status'] == 'NOT_FOUND'):
                print("Es 0")
            else:
                for i in range(directions):
                    row_times.append(result['rows'][0]['elements'][i]['duration']['value'])
                    row_distances.append(result['rows'][0]['elements'][i]['distance']['value'])

        adjacency_matrix_times.append(row_times)
        adjacency_matrix_distances.append(row_distances)

    #print(adjacency_matrix_times)
    #print(adjacency_matrix_distances)
    return adjacency_matrix_times,adjacency_matrix_distances

    
##working('driving', [], [],{1: [10.424646, -75.5408702], 2: [10.4270046, -75.5453768], 3: [10.4249692, -75.5468839], 4: [10.3932277, -75.4832311]})


