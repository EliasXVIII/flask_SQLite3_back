### Importamos sqlite3 y la llamamos con "as" como sql
import sqlite3 as sql


### con esta funcion vamos a crear la base de datos que le llamaremos libros
def createDB():
    conn = sql.connect("database/libros.db")
    conn.commit()
    conn.close()

### con esta funcion vamos a crear la base de dato y no es mas que un String ya que las bases de datos no son mas que eso.
def createTable():
    conn = sql.connect("database/libros.db")
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
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO books VALUES ({id}, '{title}', '{year}', {score})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


### Ahora voy a crear una funcion para mostrar los datos de los libros. basicamente para poder leer estos en la base de datos.

def readBook():
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM books"
    cursor.execute(instruccion) ### Es lo mismo que la de crear solo que cambia la instruccion.
    datos = cursor.fetchall() ###el fetchall hace un recorrido de todos los datos.
    conn.commit()
    conn.close()
    print(datos)


### Ahora esta función sirve para agregar muchos datos a la vez, o sea muchas filas a la vez. NO linea por linea. 
def insertBooks(booksList):
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO books VALUES (?, ?, ?, ?)" 
    cursor.executemany(instruccion, booksList) ### usamos executemany porque son varios datos.
    conn.commit()
    conn.close()



### vamos a generar una consulta ordenada por los nombres de los libros o por el año o el score
def readOrdered(field):
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM books ORDER BY {field}"
    cursor.execute(instruccion)
    datos = cursor.fetchall() 
    conn.close()
    print(datos)





### Vamos a crear una consulta para el WHERE 

def search():
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM books WHERE title='Drácula'"
    cursor.execute(instruccion)
    datos = cursor.fetchall() 
    conn.close()
    print(datos)


def searchLike():
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM books WHERE title like 'FRANKENSTEIN'"
    cursor.execute(instruccion)
    datos = cursor.fetchall() 
    conn.close()
    print(datos)


### Ahora vamos a actualizar los datos que tenemos en tabla con esta función para que si necesitamos modificar o actualizar datos.

def updateFields():
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"UPDATE books SET year='2000' WHERE title='El señor de las moscas'"
    cursor.execute(instruccion) 
    conn.commit()
    conn.close()


### Ahora vamos a eliminar datos en tabla con esta función
def deleteRows():
    conn = sql.connect("database/libros.db")
    cursor = conn.cursor()
    instruccion = f"DELETE FROM books WHERE title='Drácula'"
    cursor.execute(instruccion) 
    conn.commit()
    conn.close()





### Con esta instruccion solo ejejuta si estoy dentro de este archivo.
if __name__ == "__main__":
    """ createDB() """ ###Comentado ya que el siguiente paso es ejecutar createTable()
### desde aca la ejecutamos.
    """ createTable() """

""" insertBook(1, "Frankenstein", "1961", 278) """
""" insertBook(2, "Los viajes de Gulliver", "1921", 269) """
""" insertBook(3, "El conde de Montecristo", "sigo XX", 267) """
""" readBook() """
### al ejecutar readBook() nos da los siguiente
### [(1, 'Frankenstein', '1961', 278), (2, 'Los viajes de Gulliver', '1921', 269), (3, 'El conde de Montecristo', 'sigo XX', 267)]
### nos da listas por los [] y dentro de esta nos da tuplas y cada tupla contiene los campos de cada fila.


### Ahora vamos a insertar muchos datos a la vez.
""" booksList = [
    (4, "Los juegos del hambre", "1934", 295),
    (5, "Harry Potter y la piedra filosofal", "1854", 293),
    (6, "El señor de las moscas", "Desconocido", 278),
    (7, "Moby Dick", "1987", 277),
    (8, "Drácula", "Siglo XVIII", 262),
    (9, "El nombre de la rosa", "Algún día", 258),
    (10, "El extranjero", "2023", 255)
]
"""
""" insertBooks(booksList) """
    ### Vamos a insertarla de la misma manera que vimos en el print de readBook() una lista de tuplas.
""" 
readOrdered("title") """
### con esta funcion vamos a ordenar por el parametro que le pasemos a readOrdered("title"||"year"|| score)
""" [(8, 'Drácula', 'Siglo XVIII', 262), 
 (3, 'El conde de Montecristo', 'sigo XX', 267), 
 (10, 'El extranjero', '2023', 255), 
 (9, 'El nombre de la rosa', 'Algún día', 258), 
 (6, 'El señor de las moscas', 'Desconocido', 278), 
 (1, 'Frankenstein', '1961', 278), 
 (5, 'Harry Potter y la piedra filosofal', '1854', 293), (4, 'Los juegos del hambre', '1934', 295), 
 (2, 'Los viajes de Gulliver', '1921', 269), 
 (7, 'Moby Dick', '1987', 277)] """


""" search() """
### en nuestro print nos devuelve esto la consulta WHERE 
""" [(8, 'Drácula', 'Siglo XVIII', 262)] """

""" searchLike() """

""" updateFields() """
pass
