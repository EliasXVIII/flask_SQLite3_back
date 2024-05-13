from flask import Flask, jsonify, request, render_template
from sqlalchemy import or_ ##Render template nos ayuda a publicar o enlazar el html

##Ahora vamos a importar el formato de tabla que hemos creado en Models.py
from Models import db, books
from logging import exception
import requests

app = Flask(__name__) ## Entre guiones el nombre del fichero actual.


####### Esto pertenece a JWT #####
from routes.auth import routes_auth
from dotenv import load_dotenv
####### Esto pertenece a JWT #####


####### Esto pertenece a JWT #####
app.register_blueprint(routes_auth, url_prefix="/api")
####### Esto pertenece a JWT #####


##vamos a conectar la app con la base de datos con alchemy 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/libros.db"

## Con esta linea vamos a limpiar la consola a la hora de las consultas
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  ##Esto es para que sepa donde debe iniciar la base de datos 


###Vamos a crear un decorador con las rutas de todas las paginas que estamos creando.###
@app.route("/")
def home():##Aca ca funcion debe llamarse diferente para que estas no se solapen y den errores.
    return render_template("index.html") ## El render_template es una función que uso para renderizar los html que guardo en la carpeta templates.

@app.route("/search.html", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/delete.html", methods=["GET"])
def delete():
    return render_template("delete.html")

@app.route("/edit.html", methods=["GET"])
def edit():
    return render_template("edit.html")




@app.route("/api/v1/books", methods=["GET"])
def getBooks():
    try:
        booksList = books.query.all()
        toReturn = [book.serialize() for book in booksList]
        return jsonify(toReturn), 200

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
    

## Ahora voy a crear la ruta para agregar todos los datos que voy a incorporar por el formulario de agregar libros que se encuentra en el index.html
@app.route("/api/addbook", methods=["POST"]) ##Aca tengo un decorador con la ruta y el motodo POST 
def addBook():
    try:
        title = request.form["title"]##con request estoy reqiiriendo los datos desde el formulario y accedo al dato title por ej, y lo agrego a la variable title.
        year = request.form["year"]
        score = request.form["score"]

        newBook = books(title,year,int(score))##En esta parte almaceno en newBook, todos los datos requeridos con los datos(title,year,int(score)) almacenados en books(asi se llama mi base de datos)
        db.session.add(newBook) ##entonces en newBook sera agregado (add) en al db (base de datos)
        db.session.commit()## y el commit es para subir estos cambios como en GIT

        return jsonify(newBook.serialize()), 200 ##Aca estamos convirtiendo el objeto newBook a un formato json utilizando la función jsonify y mi db tiene un serialize() que convierte el objeto {} a un diccionario, esta línea convierte ese diccionario a json.
    
    except Exception:
        exception("\n [SERVER]: Error en la ruta /api/addbook. log: \n") ##Este exception es el que nos da el error en el servidor, no se lo muestra al usuario.
        return jsonify({"message": "Error al cargar el libro!!"}), 500 ## y este es el error que ve el usuario.





## Aca voy a crear la funcion para buscar libros a traves del fomulario creado en templates en search.html

@app.route("/api/search", methods=["POST"])
def searchBook():
    try:
        titleBook = request.form["title"]##Aca voy a guardar en titleBook lo que me envíe el input del formulario
        book = books.query.filter(books.title.like(f"%{titleBook}%")).first()##Y aca lo voy a filtrar de la base de datos de books y con la funcion like me buscará aunque sea aproximado el imput y lo hara coincidir con el primer resultado que encuentre y lo almaceno en book
        if not book:
            return jsonify({"message": "No se ha encontrado el libro"}), 404
        else:
            return jsonify(book.serialize()), 200 ## Ene ste if hago que si no resuelve la variable book, significa que no hay nad parecido y dice que no hay libro en cambio si hay, paso al else y devuelvo un json con el resultado de ese libro serializado con todos sus datos.
    except Exception:
        exception("Falla el servidor!! ")
        return jsonify({"message": "Falla el servidor!!"}), 500


### Este es metodo delete para borrar los libros. 

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

##
@app.route("/api/updatebook", methods=["PUT"])
def updateBook():
    try:
        # Obtener los datos del libro a modificar del cuerpo de la solicitud PUT
        title = request.form["title"]
        new_year = request.form["new_year"]
        new_score = request.form["new_score"]

        # Buscar el libro por su título en la base de datos
        book = books.query.filter_by(title=title).first()
        if not book:
            # Si el libro no existe, que de un mensaje de error
            return jsonify({"message": "El libro no existe"}), 404

        # Actualizar los datos del libro con los nuevos valores
        book.year = new_year
        book.score = new_score

        # Guardar los cambios en la base de datos
        db.session.commit()

        # Devolver un mensaje de éxito
        return jsonify({"message": "Libro actualizado exitosamente"}), 200

    except Exception as e:
        # Si ocurre algún error durante el proceso, devuelve un mensaje de error interno del servidor
        exception(f"Falla en el servidor al actualizar el libro: {str(e)}")
        return jsonify({"message": "Error interno del servidor al actualizar el libro"}), 500

##############3 Este es para consultar a través de postman
@app.route("/api/updatebook", methods=["PUT"])
def updateBookPostman():
    try:
        # Obtener los datos del libro a modificar del cuerpo de la solicitud PUT
        title = request.args.get("title")
        new_year = request.args.get("new_year")
        new_score = request.args.get("new_score")

        # Buscar el libro por su título en la base de datos
        book = books.query.filter_by(title=title).first()
        if not book:
            # Si el libro no existe, devuelve un mensaje de error
            return jsonify({"message": "El libro no existe"}), 404

        # Actualizar los datos del libro con los nuevos valores
        book.year = new_year
        book.score = new_score

        # Guardar los cambios en la base de datos
        db.session.commit()

        # Devolver un mensaje de éxito
        return jsonify({"message": "Libro actualizado exitosamente"}), 200

    except Exception as e:
        # Si ocurre algún error durante el proceso, devuelve un mensaje de error interno del servidor
        exception(f"Falla en el servidor al actualizar el libro: {str(e)}")
        return jsonify({"message": "Error interno del servidor al actualizar el libro"}), 500

if __name__ == "__main__":
    ####### Esto pertenece a JWT #####
    load_dotenv()
    ####### Esto pertenece a JWT #####
    app.run(debug=True, port="4000", host="0.0.0.0")