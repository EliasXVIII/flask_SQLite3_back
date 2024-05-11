from flask import Flask, jsonify, request, render_template, url_for
from sqlalchemy import or_ ##Render template nos ayuda a publicar o enlazar el html

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
def home():
    return render_template("index.html")

@app.route("/search.html", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/delete.html", methods=["GET"])
def delete():
    return render_template("delete.html")


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
    

## Ahora voy a crear la ruta para agregar todos los datos que voy a incorporar por el formulario.
@app.route("/api/addbook", methods=["POST"])
def addBook():
    try:
        title = request.form["title"]
        year = request.form["year"]
        score = request.form["score"]

        newBook = books(title,year,int(score))
        db.session.add(newBook)
        db.session.commit()

        return jsonify(newBook.serialize()), 200
    
    except Exception:
        exception("\n [SERVER]: Error en la ruta /api/addbook. log: \n")
        return jsonify({"message": "Error al cargar el libro!!"}), 500


## Aca voy a crear la funcion para buscar libros a traves del fomulario creado en templates


@app.route("/api/search", methods=["POST"])
def searchBook():
    try:
        titleBook = request.form["title"]
        book = books.query.filter(books.title.like(f"%{titleBook}%")).first()
        if not book:
            return jsonify({"message": "No se ha encontrado el libro"}), 404
        else:
            return jsonify(book.serialize()), 200
    except Exception:
        exception("Falla el servidor!! ")
        return jsonify({"message": "Falla el servidor!!"}), 500

@app.route("/api/delete", methods=["DELETE"])
def deleteBook():
    try:
        # Obtener el título del libro de la solicitud DELETE
        title = request.args.get("title")

        # Buscar el libro por su título en la base de datos
        book = books.query.filter_by(title=title).first()
        if not book:
            # Si el libro no existe, devuelve un mensaje de error
            return jsonify({"message": "El libro no existe"}), 404
        
        # Eliminar el libro de la base de datos
        db.session.delete(book)
        db.session.commit()

        # Devolver un mensaje de éxito
        return jsonify({"message": "Libro eliminado exitosamente"}), 200

    except Exception as e:
        # Si ocurre algún error durante el proceso, devuelve un mensaje de error interno del servidor
        exception(f"Falla en el servidor al eliminar el libro: {str(e)}")
        return jsonify({"message": "Error interno del servidor al eliminar el libro"}), 500



if __name__ == "__main__":
    ####### Esto pertenece a JWT #####
    load_dotenv()
    ####### Esto pertenece a JWT #####
    app.run(debug=True, port="4000", host="0.0.0.0")