# Import
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from random import sample, randint, uniform
import math,json,time,urllib.parse,urllib.request
from flask_googlemaps import GoogleMaps,Map
from recocido import workinghard
from unidecode import unidecode

# Init
app = Flask(__name__)

# Configuraciones de la app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/places.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
key = 'AIzaSyBwogYJ7xQkoQ-lunCXWsobGvLxU9fayIk'
base_url_geocoding = 'https://maps.googleapis.com/maps/api/geocode/json?address='
base_url_distance_matrix = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='
base_url_distance = 'https://maps.googleapis.com/maps/api/directions/json?origin='
app.config['GOOGLEMAPS_KEY'] = key

# Se inicializa la extension para usar google maps
GoogleMaps(app)

# Antes de la primera request se crea la base de datos, con sus atributos
@app.before_first_request
def create_tables():
    db.create_all()

# Class DataModel
# @arg Object
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(200))
    lat = db.Column(db.String(200))
    lngd = db.Column(db.String(200))

#Ruta inicial del home
@app.route('/')
def index():
    data = Place.query.all()
    return render_template('index.html', data=data)

#ruta para guardar dentro de la base de datos los datos que se manden desde el formulario de la vista
@app.route('/saveplace', methods=['POST'])
def add_place():
	# POST
	if request.method == 'POST':
		locate = request.form['place']
		gloc = unidecode(locate) #se transforma el dato para buscar en api y que retorne su ubicacion
		ngloc = gloc.replace(' ', '+')
		url_geocoding = base_url_geocoding + 'cartagena' +'%'+'colombia' + ngloc + 'CA&key=' + key
		response = urllib.request.urlopen(url_geocoding)
		result = json.loads(response.read().decode())
		if result['status'] == 'OK': 
			lat = str(result['results'][0]['geometry']['location']['lat'])
			lngd = str(result['results'][0]['geometry']['location']['lng'])
			place = Place(place=locate, lat=lat, lngd=lngd)
			db.session.add(place)
			db.session.commit()

	return redirect(url_for('index'))
	
#Ruta request de forma get para obtener el mapa con los locaciones de los lugares que estan dentro de la base de datos
@app.route('/api/showmap', methods=['GET'])
def showmap():
	places = Place.query.all()
	markers_loc =[{"lat":float(i.lat), "lng":float(i.lngd), "infobox": i.place} for i in places]
	return render_template('map.html', data=markers_loc)


#Selecciona una opcion antes de calcular la ruta más optima con el recocido simulado
#Solo es una acción que redirecciona al template que luego calcula la ruta
@app.route('/shortpath/<string:option>')
def wait(option):
	places = Place.query.all()
	if(places):
		keys= [int(i.id) for i in places]
		values = [[float(i.lat),float(i.lngd)] for i in places]
		for i in places:
			placesdict= dict(zip(keys,values))
		dplaces= placesdict
		jplaces = jsonify(placesdict)
	if(option=="json"):
		return(jplaces)
	else:
		return render_template('wait.html',option=option)


#Con el temporizador y la opción pasada de la ruta anterior retorna el mapa con la ruta más óptima
@app.route('/shortpath/<string:option>/<string:timer>')
def shortpath(option,timer):
	places = Place.query.all()
	if(places):
		newplaces =[]
		keys= [int(i.id) for i in places]
		values = [[float(i.lat),float(i.lngd)] for i in places]
		for i in places:
			placesdict= dict(zip(keys,values))
		dplaces= placesdict
		jplaces = jsonify(placesdict)
		#Desde aquí se calcula la ruta más optima con el microservicio del recocido simulado
		if (option == "driving" or option =="walking"):
			recorrido,tiempo,distancia = workinghard(option,dplaces,int(timer),10000)
		else:
			if option == "json":
				return(jplaces)	
			else:
				timer = '5' #default
				option = "driving" #default
				recorrido,tiempo,distancia = workinghard(option,dplaces,int(timer),10000)

		#Luego que se obtiene la ruta se hacen los map markers para dibujar una aproximación de la ruta exacta en el mapa
		for i in recorrido:
			newplaces.append(Place.query.filter_by(id=i).one())
	
		newrecorrido = [i.place for i in newplaces]
		
		tiempomin = round(tiempo/60,2)

		#marcadores para dibujar la ruta
		mark =[{"lat":i.lat, "lng":i.lngd, "infobox":i.place} for i in newplaces]
		markes = [{"lat": float(i.lat), "lng":float(i.lngd)} for i in newplaces]
		markers_loc = []

		for i in range(len(mark)-1):
			url_directions = base_url_distance + mark[i]['lat'] + ',' + mark[i]['lng'] +'&destination=' + mark[i+1]['lat'] + ',' + mark[i+1]['lng'] +'&key=' + key
			response = urllib.request.urlopen(url_directions)
			result = json.loads(response.read().decode())
			if result['status'] == 'OK':
				markers_loc = pathfresh(result['routes'][0]['legs'][0]['steps'],markers_loc)
		
		#Se dibuja la linea que se mostrará en la vista web dentro del mapa
		polyline={
			"stroke_color": "#108db0",
			"stroke_opacity": 1.0,
			"stroke_weight": 4,
			"path": markers_loc,
		}	

		#Se crea el mapa con Flask-googlemaps y se pasan los parametros a la respectiva template
		plinemap = Map(
			identifier="plinemap",
			varname="plinemap",
			lat=markers_loc[0]['lat'],
			lng=markers_loc[0]['lng'],
			polylines=[polyline]
		)
		return render_template('shortpath.html',markers=mark,polyline=polyline,tiempomin=tiempomin,distancia=round(distancia,2),precorrido=newrecorrido)
	else:
		return redirect(url_for('index'))

#Funcion que seleccione de la respuesta a la request cada longitud y latitud en cada paso que da la ruta
def pathfresh(pathact,path):
	for i in pathact:
		path.append(i['start_location'])
		path.append(i['end_location'])
	return path


# Borra un lugar de la base de datos
@app.route('/delete/<string:id>')
def delete(id):
	Place.query.filter_by(id=id).delete()
	db.session.commit()
	return redirect(url_for('index'))

#Borra todos los lugares de la base de datos
@app.route('/deleteall')
def deleteall():
	Place.query.delete()
	db.session.commit()
	return redirect(url_for('index'))

# Main
if __name__ == "__main__":
    app.run(debug=True)
