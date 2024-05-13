### de JWT vamos a importar
import token
from jwt import encode, exceptions, decode
### el os import getenv es para traer el SECRET de .env
from os import getenv

from flask import jsonify

## voy a importar la fecha actual para hacer el calculo de expiración
from datetime import datetime, timedelta

### encode(playload={**data, "exp"=> nos pide un tiempo de expiracion
# para eso vamos a crear una funcion en la que vamos a calcular ese tiempo.

def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days) 
    return new_date


## vamos a crear una funcion va a recibir el data que va a ser de tipo diccionario.
def write_token(data: dict):
    ###ahora vamos a llamar a encode() y esa funcion va a recibir lo que va encripta con payload y luego el KEY que es la info con la que va a encriptar ese valor
    token = encode(payload={**data, "exp":expire_date(2)}, key=getenv("SECRET"), algorithm="HS256")
    return token.decode("UTF-8") ##en casa tengo que usar encode!!!! OJO!!! 

## Ahora vamos a crear una funcion para validar y esta funcion va a recibir el token y si queire demostrar la salida. 

def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token,key=getenv("SECRET"), algorithm=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "El token no es valido"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "El token ha expirado"})
        response.status_code = 401
        return response


""" Ahora vamos a crear las rutas por que no las queremos tener en el archivo principal """