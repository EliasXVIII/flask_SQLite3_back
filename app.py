from flask import Flask

app = Flask(__name__) ## Entre guiones el nombre del fichero actual.

##vamos a conectar la app con la base de datos con alchemy
app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///database\\libros.db"

## Con esta linea vamos a limpiar la consola a la hora de las consultas
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

