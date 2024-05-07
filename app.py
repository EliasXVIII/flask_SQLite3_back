from flask import Flask, jsonify
##Ahora vamos a importar el formato de tabla que hemos creado en Models.py
from Models import db, books
from logging import exception

app = Flask(__name__) ## Entre guiones el nombre del fichero actual.

##vamos a conectar la app con la base de datos con alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/libros.db"

## Con esta linea vamos a limpiar la consola a la hora de las consultas
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  ##Esto es para que sepa donde debe iniciar la base de datos """



#Vamos a crear un decorador
@app.route("/")
def hello_world():
    return "<h1>My Books!</h1>"

@app.route("/api/v1/books")
def getBooks():
    try:
        booksList = books.query.all()
        toReturn = [book.serialize() for book in booksList]
        return jsonify(toReturn), 200 ## el 200 es el codigo de respuesta. el jsonify nos devuelve el bucle for hecho json.

    except Exception:
        exception("Falla el servidor!! ")
        return jsonify({"message": "Falla el servidor!!"}), 500 ## 



if __name__ == "__main__":
    app.run(debug=True, port=4000)