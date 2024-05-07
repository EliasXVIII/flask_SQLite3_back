### Importamos sqlite3 y la llamamos con "as" como sql
import sqlite3 as sql

### Ahora almacenamos en una variable la ruta relativa de la base de datos.
""" DB_PATH = "/home/alumno/flask_SQLite3_back/database/seeder.py" """

### con esta funcion vamos a crear la base de datos que le llamaremos libros
def createDB():
    conn = sql.connect("libros.db")
    conn.commit()
    conn.close()

### con esta funcion vamos a crear la base de dato y no es mas que un String ya que las bases de datos no son mas que eso.
def createTable():
    conn = sql.connect("libros.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year TEXT NOT NULL,
        score INTEGER NOT NULL
        )"""
    )
    conn.commit()
    conn.close()

    ### vamos a llamar al metodo commit (realizar los cambios) y cerramos la coneccion, vamos a ejecutar esta funcion abajo de createDB()


### Ahora voy a crear una funcion para insertar los datos de los libros.
def insertBook(id, title, year, score):
    conn = sql.connect("libros.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO books VALUES ({id}, '{title}', '{year}', {score})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


### Ahora voy a crear una funcion para mostrar los datos de los libros. basicamente para poder leer estos en la base de datos.

def readBook():
    conn = sql.connect("libros.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM books"
    cursor.execute(instruccion) ### Es lo mismo que la de crear solo que cambia la instruccion.
    datos = cursor.fetchall() ###el fetchall hace un recorrido de todos los datos.
    conn.commit()
    conn.close()
    print(datos)


### Ahora esta función sirve para agregar muchos datos a la vez, o sea muchas filas a la vez. NO linea por linea. 
def insertBooks(booksList):
    conn = sql.connect("libros.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO books VALUES (?, ?, ?, ?)" 
    cursor.executemany(instruccion, booksList) ### usamos executemany porque son varios datos.
    conn.commit()
    conn.close()








### Con esta instruccion solo ejejuta si estoy dentro de este archivo.
if __name__ == "__main__":
    """ createDB() """ ###Comentado ya que el siguiente paso es ejecutar createTable()
### desde aca la ejecutamos.
    """ createTable() """

"""   insertBook(1, "Frankenstein", "1961", 278) """
""" insertBook(2, "Los viajes de Gulliver", "1921", 269) """
""" insertBook(3, "El conde de Montecristo", "sigo XX", 267) """
""" readBook() """
### al ejecutar readBook() nos da los siguiente
### [(1, 'Frankenstein', '1961', 278), (2, 'Los viajes de Gulliver', '1921', 269), (3, 'El conde de Montecristo', 'sigo XX', 267)]
### nos da listas por los [] y dentro de esta nos da tuplas y cada tupla contiene los campos de cada fila.


### Ahora vamos a insertar muchos datos a la vez.
booksList = [
    (4, "Los juegos del hambre", "1934", 295),
    (5, "Harry Potter y la piedra filosofal", "1854", 293),
    (6, "El señor de las moscas", "Desconocido", 278),
    (7, "Moby Dick", "1987", 277),
    (8, "Drácula", "Siglo XVIII", 262),
    (9, "El nombre de la rosa", "Algún día", 258),
    (10, "El extranjero", "2023", 255)
]

insertBooks(booksList)
    ### Vamos a insertarla de la misma manera que vimos en el print de readBook() una lista de tuplas.