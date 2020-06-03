# Autores
- Maria Villamizar
- Jesus Caraballo


# Requerimientos
- Python
- Flask
- Docker (optional)

# Guía simple de desarrollo
## Antes de iniciar
```sh
  # Clone
  $ git clone https://github.com/camiilavillamizar/Betterpath.git
  $ cd Betterpath
```
- De otra forma asegurate de que escribas las instrucciones que siguen dentro de la carpeta donde guardaste este proyecto.
- Recuerda seleccionar el interprete de Python de la carpeta `venv`.

## Instrucciones para Docker 
### 1. Ejecutar y actualizar
```sh
  # Se crea una imagen
  $ docker build -t "image-name" .

  # Se crea un contenedor de la imagen
  $ docker run -p 5000:5000 "image-name"
```

### 2. Reiniciar
```sh
  # Detener todos los contenedores
  $ docker stop $(docker ps -q)

  # Se eliminan todos los contenedores
  $ docker rm $(docker ps -aq)
```

## Intrucciones directas para consola
### 1. Preparar
```sh
  # Installar el ambiente virtual
  $ python3 -m venv venv

  # Installar el ambiente virtual (en Windows)
  $ py -3 -m venv venv

# Installar el ambiente virtual (Otra opción para Windows)
  $ python3 -m venv venv

  # Activar el ambiente virtual
  $ . venv/bin/activate

  # Activar el ambiente virtual (en Windows)
  $ venv\Scripts\activate

  # Instalar todas las dependencias
  $ pip install -U -r requirements.txt

```

### 2. Ejecutar
```sh
  # Configurar la aplicación Flask 
  $ export FLASK_APP=app.py

  # Configurar la aplicación Flask (en Windows)
  $ set FLASK_APP=app.py

  # Modo de desarrollo
  $ export FLASK_ENV=development

  # Modo de desarrollo (en Windows)
  $ set FLASK_ENV=development

  # Ejecutar
  $ flask run

  # Go to http://127.0.0.1:5000
```

# Registro simple de cambios

## [1.0.0]
- Miligram (framework CSS) para la vista.
- Se inicia la aplicación con Flask Python.
- `readme` detallado.
- Completado el `Dockerfile`.
- uso del Modelo Vista Controlador.
- Agregado el microservicio para el recocido simulado.
- Agregado el microservicio para calcular las matrices de adyascencia.
- Vista de mapas con GoogleMaps.
- Uso de SQLAlchemy para crear el modelo de base de datos.
