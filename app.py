from flask import Flask, jsonify, request
##Ahora vamos a importar el formato de tabla que hemos creado en Models.py
from Models import db, books
from logging import exception
import requests

####### Esto pertenece a JWT #####
from routes.auth import routes_auth
from dotenv import load_dotenv
####### Esto pertenece a JWT #####



app = Flask(__name__) ## Entre guiones el nombre del fichero actual.

####### Esto pertenece a JWT #####
app.register_blueprint(routes_auth, url_prefix="/api")
####### Esto pertenece a JWT #####





##vamos a conectar la app con la base de datos con alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/libros.db"

## Con esta linea vamos a limpiar la consola a la hora de las consultas
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  ##Esto es para que sepa donde debe iniciar la base de datos """



#Vamos a crear un decorador
@app.route("/")
def hello_world():
    return "<h1>My Books en Libros.db!</h1>"




@app.route("/api/v1/books", methods=["GET"])
def getBooks():
    try:
        booksList = books.query.all()
        toReturn = [book.serialize() for book in booksList]
        return jsonify(toReturn), 200 ## el 200 es el codigo de respuesta. el jsonify nos devuelve el bucle for hecho json.

    except Exception:
        exception("Falla el servidor!! ")
        return jsonify({"message": "Falla el servidor!!"}), 500




@app.route("/api/v1/book", methods=["GET"])
def getBookByTitle():
    try:
        titleBook = request.args["title"]
        book = books.query.filter_by(title=titleBook).first()
        if not book:
            return jsonify({"message": "No se ha encontrado el libro"}), 404
        else:
            return jsonify(book.serialize()), 200

    except Exception:
        exception("Falla el servidor!! ")
        return jsonify({"message": "Falla el servidor!!"}), 500


@app.route("/api/v1/findbook", methods=["GET"])
def getBook():
    try:
        fields = {}
        if "title" in request.args:
            fields["title"] = request.args["title"]

        if "year" in request.args:
            fields["year"] = request.args["year"]

        if "score" in request.args:
            fields["score"] = request.args["score"]

        book = books.query.filter_by(**fields).first()
        if not book:
            return jsonify({"message": "No se ha encontrado el libro"}), 404
        else:
            return jsonify(book.serialize()), 200

    except Exception:
        exception("Falla el servidor!! ")
        return jsonify({"message": "Falla el servidor!!"}), 500
    




if __name__ == "__main__":
    ####### Esto pertenece a JWT #####
    load_dotenv()
    ####### Esto pertenece a JWT #####
    app.run(debug=True, port="4000", host="0.0.0.0")