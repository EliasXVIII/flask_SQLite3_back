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
    token = encode(playload={**data, "exp":expire_date(2)}, key=getenv("SECRET"), algorithm="HS256")
    return token.encode("UTF-8")

## Ahora vamos a crear una funcion para validar y esta funcion va a recibir el token y si queire demostrar la salida. 

def valida_token(token, output=False):
    try:
        if output:
            return decode(token,key=getenv("SECRET"), algorithm=["HS256"])
        decode(token,key=getenv("SECRET"), algorithm=["HS256"])
    except exceptions.ExpiredSignatureError:
        return jsonify({"message": "El token ha expirado"}), 401
    except exceptions.InvalidSignatureError:
        return jsonify({"message": "El token no es valido"}), 401
    except exceptions.DecodeError:
        return jsonify({"message": "El token no es valido"}), 401


""" Ahora vamos a crear las rutas por que no las queremos tener en el archivo principal """