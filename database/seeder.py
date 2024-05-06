### Importamos sqlite3 y la llamamos con "as" como sql
import sqlite3 as sql

### Ahora almacenamos en una variable la ruta relativa de la base de datos.
""" DB_PATH = "/home/alumno/flask_SQLite3_back/database/seeder.py" """

### con esta funcion vamos a crear la base de datos que le llamaremos libros
def createDB():
    conn = sql.connect("libros.db")
    conn.commit()
    conn.close()



### Con esta instruccion solo ejejuta si estoy dentro de este archivo.
if __name__ == "__main__":
    createDB()
### desde aca la ejecutamos.
