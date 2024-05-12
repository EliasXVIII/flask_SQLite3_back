""" https://www.youtube.com/watch?v=4mRZ3sZ8Qvc """

##En este archivos vamos a colocar las rutas.
## vamos a crear un endpoint que se llamara LOGIN y vamos a autenticarnos y nos devolvera el Token.

## Vamos a usar la calse Blueprint que viene de Flask 
from flask import Blueprint, jsonify, request

from function_jwt import write_token, validate_token


routes_auth = Blueprint("routes_auth", __name__)## aca Blueprint recibe el nombre de routes_auth y guardamos esta varialble en routes_auth

@routes_auth.route("/login", methods=["POST"]) ##vamos a crear una ruta para la autenticacion o login con el routes_auth que creamos antes y le aplicamos la ruta(route y dentro la ruta y el metodo "post" en este caso.)
def login(): ## ene sta funcion vamos  meter la solicitud de usuario y contraseña y para esto tenemos que importar request en la cabeza de pagina
    data = request.get_json() #con esto almaceno en data el usuario y pass sin usar base de datos. 
    if data["username"] == "Elias Riquelme":
        return write_token(data=request.get_json())
    else:
        response = jsonify({"message":"invalid username"})
        response.status_code = 404
        return response
    
    """ ahora vamos a cargar la variable de entorno en main.py o app.py """

@routes_auth.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)

""" https://www.youtube.com/watch?v=3o4vEIkiRgE """