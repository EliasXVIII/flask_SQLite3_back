from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class books(db.Model): ## Esto indica que es una clase de tipo modelo
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    ### aca vamos a replicar la tabla.
    ## colocamos tal cual "id" luego que de db.column => que tipo de valor si Integer o String(200 para limitar la cantidad de letras) y nullable false para que este no este vacio.

