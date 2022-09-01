# Demo "Recomendaciones de Películas"

> Integración de API RESTful, desarrolado con Flask y Vue JS 2

Proyecto de demostración, desarrollado para dar recomendaciones de películas a los usuarios que navegen por el sitio web, retroalimentado por los usuarios que deseen registrar películas en el sitio web.

## Características

- CRUD de Recursos implementado con Marsmallow y SQLAlchemy
- Tramamiento de excepción de errores y códigos de estado HTTP
- Migración de Modelo de base datos con Flask DB Migrate
- Versionamiento de API-RESTful
- Habilitación de CORS con Flask Cors
- Envio de petición de cambio de contraseñas de usuaruarios vía correo electronico

## Librerías

Cartelera CMVP, esta desarrollada con las siguientes extensiones.
Las instrucciones de como usarlas en tu propias aplicaciones estan en la siguiente tabla.

| Librería | Documentación |
| ------ | ------ |
| FLask | [Documentación][LinkFlask] |
| Flask-Cors | [Documentación][LinkFlaskCors] |
| Flask RestFul | [Documentación][LinkFlaskRestful] |
| Flask SQLAlchemy | [Documentación][LinkFlaskSQLAlchemy] |
| Flask Mail | [Documentación][LinkFlaskMail] |
| Flask Migrate | [Documentación][LinkFlaskMigrate] |
| Flask Marshmallow | [Documentación][LinkFlaskMarshmallow] |
| Marshmallow SqlAlchemy | [Documentación][LinkMarshmallowSQLAlchemy] |
| Python DotoEnv | [Documentación][LinkDotoEnv] |
| PyJWT | [Documentación][LinkPyJWT] |
| uuid | [Documentación][LinkUUUID] |

## Instalación
Dentro de la ruta local de tu computador en donde desees obtener una copia de este repositorio, coloca la siguiente instrucción en el CLI de Git:

    git clone https://github.com/litocmvp/demo_movies_backend.git

Una vez obtenido procedemos a entrar al directorio del repositorio por CLI y creamos un entorno virtual en Python (preferentemente en la versión 3.10). con el siguiente comando:

    python3 -m venv enviroment_name # En Linux / MacOS
    py -3 -m venv enviroment_name # En Windows

__Nota:__ *"enviroment_name" se refiere al nombre que deseemos colocarle al entorno virtual*

Al crearse procedemos a entrar al entorno virtual con la siguiente instrucción:

    . enviroment_name/bin/activate # En Linux / MacOS
     enviroment_name\Scripts\activate # En Windows
Ya adentro del entorno virtual , procedemos a instalar los requerimientos con la instrucción:

    pip3 install -r requeriments.txt # En Linux / MacOS
    pip install -r requeriments.txt # En Windows
Ya instalado los requerimientos, podremos estar a un paso de ejecutar la aplicación, solo nos faltaría, declarar las siguientes variables del entorno virtual, en el CLI:

	    FLASK_APP = "entrypoint:app"
	    FLASK_ENV = "development" # Opcional
	    FLASK_RUN_PORT = 8081
	    APP_ENV = "config.dev"

__Nota:__
- En Linux / MacOS usar: "export EnviromentName"
- En Windows (PowerShell) usar: "$env:EnviromentName"

### Pre-requisitos

Para que la aplicación funcione de manera optima, requerirá crear un archivo llamado ".env", que almacenará otras variables de entorno esenciales para la aplicación, los cuales se encuentrán detallados en los archivos "dev.py" y "prod.py", de la carpeta "config".
Los nombres de las variables de entorno que deberas colocar en el archivo ".env" son los siguientes:

 - KEY
 - DB_URL
 - MAIL_SERVER
 - MAIL_PORT
 - MAIL_USER
 - MAIL_PASS
 - MAIL_DONT_REPLY
 - MAIL_ADMIN
 - WEBSITE

 En donde "KEY" será una clave secreta para uso de la aplicación en Flask, la cual podrá ser cualquier contraseña que desees ej. "12345_esta_es_mi_password" o si deseas generar una aleatoria, sigue las siguientes instrucciones en un CLI:

    py
    import os
    print(os.urandom(byte_length))
__Nota:__ *"byte_length" es el número de longitud de la cifra que deseemos, ej: 24*

Como resultado el CLI nos imprimiría por ejemplo este resultado: `b'KG\xe2"\x89\xb4\x88G\x05\x91\x8bWLdu$1\xdc\x84\x00\x8b\xbe5\x9d'`
El cual podrías usar para el valor de la variable KEY.

La variable "PATH_DB" se refiere a la ruta o dirección de conexión de la base de datos, como consejo, sugiero que uses sqlite para esta demo, por ejemplo podrias colocar el siguiente valor a esta variable, como ruta de la base de datos:

    # En Linux / MacOS
	    'sqlite://///home/username/repositoryfolder/db_prueba.db'
    # En Windows
	    'sqlite:///C:\\Users\\UserName\\Desktop\\RepositoryFolder\\db_prueba.db'

Las variables "MAIL_*" se refieren a los datos de su dirección de correo, que funcionará como correo saliente para las pruebas de envio de correo en peticiones de cambio de contraseña.

La Variable WEBSITE, solo es la dirección url del sitio, en donde se alojará el sitio web del lado frontend.

Ya creado el archivo ".env" dentro de la carpeta del repositorio, como ultimo y para que surtan efectos estas variables, necesitaremos salir del entorno virtual, previamente creado y volver a ingresar, para detectar las variables de entorno dentro del archivo ".env"; esto lo logramos con la siguiente instrucción en el CLI:

    deactivate
    . enviroment_name/bin/activate # En Linux / MacOS
     enviroment_name\Scripts\activate # En Windows

### Creación de Tablas
Es igual necesario crear la Base de datos (solamente vacía) antes de ejecutar la aplicación, para que el PATH_DB, localice la BD y pueda leer las tablas, que se crearán a continuación siguiendo las siguientes instrucciones, dentro de la ruta del repositorio en el CLI:

    flask db init
    flask db migrate -m "Inciando Migración de tablas por primera vez"
    flask db upgrade
Con estas tres instrucciones podemos generar las tablas dentro de la base de datos, la cual definimos su ruta en el archivo "PATH_DB"

## Ejecutando las Pruebas
Iniciamos la aplicación con el siguiente comando:

    flask run

Para consumir la API-REST, podemos implementar en contraparte el ["respositorio del proyecto frontend"][LinkFrontendRepo] ó procedemos a usar la extención ["Thunder Client"][LinkThunderClient], dentro del entorno de desarrollo de "Visual Studio Code".

### Registro de Usuario
Parametros de la petición de envio
```sh
POST http://localhost:8081/api/v1.0/user/auth
HEADER [ "Content-Type" : "application/json" ]
BODY {"user": "example@email.com", "password": "thisIsMyPassword"}
```
Respuesta del API-REST
```sh
STATUS 201
HEADER [ "Content-Type" : "application/json" ]
RESPONSE
    {
      "admin": false,
      "password": "sha256$MEsdPlgn551ugPDW$0e0d86e51d54e02d9c131758825fcf92b4caa3bda3b44bb2f85fac89bd3715be",
      "user": "example@email.com",
      "id": 4,
      "public_id": "f51aabfe-4d63-479a-99d6-66882d004c47"
    }
```

### Autentificación de Usuario
__Ejemplo de envio de datos incorrectos__
Parametros de la petición de envio
```sh
GET http://localhost:8081/api/v1.0/user/auth
HEADER
    [
        "Content-Type" : "application/json",
        "Authorization": "Basic example@email2.com:thisIsMyPassword"
    ]
```
Respuesta del API-REST
```sh
STATUS 404 NOT FOUND
HEADER [ "Content-Type" : "application/json" ]
RESPONSE
    {
      "msg": "El usuario no existe o incorrecta contraseña"
    }
```

__Ejemplo de envio de datos correctos__
Parametros de la petición de envio
```sh
GET http://localhost:8081/api/v1.0/user/auth
HEADER
    [
        "Content-Type" : "application/json",
        "Authorization": "Basic example@email.com:thisIsMyPassword"
    ]
```
Respuesta del API-REST
```sh
STATUS 202 OK
HEADER [ "Content-Type" : "application/json" ]
RESPONSE
    {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJmNTFhYWJmZS00ZDYzLTQ3OWEtOTlkNi02Njg4MmQwMDRjNDciLCJleHAiOjE2NjE5ODkyMDh9.2C-4Y1tC2n4LB-HLOazJ4KTNmS_AZAyYcfZcfD82s6k"
    }
```
Una vez obtenido el token, podremos usarlo en la Autentificación "Bearer Token", por un tiempo de vigencía de 60 minutos, establecido en el siguiente fragmento del codigo python.

```sh
    token = jwt.encode(
        {
            'public_id': user['public_id'],
		    'exp' :
			    datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        },
		current_app.config["SECRET_KEY"],
		algorithm="HS256"
	)
```

### Registro de Genero Cinematografíco
En esta demo, se establecio que los atributos clasificaciones y generos, que toda pelicula contiene, solo fueran registrados por usuarios administradores, usando el token de autentificación, recibido para el usuario "example@email.com", veamos que nos responde la API-REST al querer realizar un registro de genero cinematografíco.

Parametros de la petición de envio
```sh
POST http://localhost:8081/api/v1.0/cinema/gender
HEADER [ "Content-Type" : "application/json"]
AUTH
    [
        "Bearer": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJmNTFhYWJmZS00ZDYzLTQ3OWEtOTlkNi02Njg4MmQwMDRjNDciLCJleHAiOjE2NjE5ODkyMDh9.2C-4Y1tC2n4LB-HLOazJ4KTNmS_AZAyYcfZcfD82s6k"
    ]
BODY
    {
        "gender": "Belico",
        "description": "Peliculas que contemplan escenas de guerras y movimientos sociales procurizando la dramatización y humanidad en la historia.",
        "picture": "https://sm.ign.com/t/ign_es/screenshot/default/galeria_39g1.1280.jpg"
    }
```
Respuesta del API-REST
```sh
STATUS 403 FORBIDDEN
HEADER [ "Content-Type" : "application/json" ]
RESPONSE
    {
      "msg": "El usuario no posee los permisos suficientes para este registro, contacte a soporte"
    }
```

### Obteniendo recurso identificado por parametros de busqueda
Como ultima prueba, obtendremos los datos de cualquier pelicula, a traves de la busqueda por el campo del titulo de la pelicula, si existe o no, obtendremos una respuesta.

__Ejemplo de obtención de respuesta en recurso encontrado__
Parametros de la petición de envio
```sh
POST http://localhost:8081/api/v1.0/cinema/movie/
HEADER ["Content-Type" : "application/json"]
BODY
    {
        "page": 1,
        "title": "narnia"
    }
```
Respuesta del API-REST
```sh
STATUS 201 CREATED
HEADER [ "Content-Type" : "application/json" ]
RESPONSE
    {
      "movies":
        [
            {
              "year": 2005,
              "duration": "01:56",
              "title": "The Chronicles of Narnia: the Lion the Witch and the Wardrobe",
              "id": 1,
              "rating": 1,
              "synopsis": "Durante la Segunda Guerra Mundial, cuatro hermanos ingleses son enviados a una casa en el campo donde van a estar a salvo de los bombardeos. Un día, Lucy, la hermana pequeña, descubre un armario que la transporta a un mundo mágico llamado Narnia. Después de volver, pronto vuelve a Narnia con sus hermanos, Peter, Edmund y Susan. Allí, los cuatro se unirán al león mágico Aslan y lucharán contra la Bruja Blanca.",
              "picture": "https://images4.alphacoders.com/794/thumb-1920-794712.jpg",
              "gender":
                [
                    {
                      "id": 1,
                      "picture": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN5CGiuQ0RZVm97JawUlm0Ukn0IpwgGMX5cA&usqp=CAU",
                      "description": "Mantente alerta todo el tiempo y no dejes de observar a tus lados",
                      "gender": "Acción"
                    },
                    {
                      "id": 4,
                      "picture": "https://p4.wallpaperbetter.com/wallpaper/1014/674/494/action-adventure-fantasy-film-wallpaper-preview.jpg",
                      "description": "Adentrate en maravillosos e inolvidables lugares, en donde los limites solo son tu imaginación",
                      "gender": "Fantasía"
                    }
                ]
            },
        ],
      "preview": false,
      "next": false
    }
```

__Ejemplo de obtención de respuesta en recurso no encontrado__
Parametros de la petición de envio
```sh
OST http://localhost:8081/api/v1.0/cinema/movie/
HEADER ["Content-Type" : "application/json"]
BODY
    {
        "page": 1,
        "title": "animales fantasticos"
    }
```
Respuesta del API-REST
```sh
STATUS 404 NOT FOUND
HEADER [ "Content-Type" : "application/json" ]
RESPONSE
    {
      "msg": "Recurso no encontrado"
    }
```

## Licencia

MIT (**Software Libre**)

## Autor
Carlos Mario Vázquez Pérez

> www.cmvp.me

   [LinkFlask]: <https://flask.palletsprojects.com/en/2.2.x/>
   [LinkFlaskCors]: <https://flask-cors.readthedocs.io/en/latest/>
   [LinkFlaskRestful]: <https://flask-restful.readthedocs.io/en/latest/>
   [LinkFlaskSQLAlchemy]: <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>
   [LinkFlaskMail]: <https://pythonhosted.org/Flask-Mail/>
   [LinkFlaskMigrate]: <https://flask-migrate.readthedocs.io/en/latest/>
   [LinkFlaskMarshmallow]: <https://flask-marshmallow.readthedocs.io/en/latest/>
   [LinkMarshmallowSQLAlchemy]: <https://marshmallow-sqlalchemy.readthedocs.io/en/latest/>
   [LinkDotoEnv]: <https://pypi.org/project/python-dotenv/>
   [LinkPyJWT]: <https://pyjwt.readthedocs.io/en/stable/>
   [LinkUUUID]: <https://docs.python.org/3/library/uuid.html>
   [LinkThunderClient]: <https://www.cleveritgroup.com/blog/test-en-visual-studio-code-con-plugin-thunder-client>
   [LinkFrontendRepo]: <https://github.com/litocmvp/demo_movies_frontend>