from flask import Flask, request, url_for, redirect, abort, render_template
import mysql.connector

app = Flask(__name__)

#Ejemplo para asignar rutas.

@app.route("/")
def index():
    return "hola mundo"

# # @app.route('/post/<int:post_id>') de esta manera definimos que el valor que se pida esa de tipo entero
# @app.route('/post/<post_id>')
# def lala(post_id):
#     return 'El id del post es: ' +  ' ' + post_id
#
# @app.route('/lele')
# def lele():
#     return 'lele'

# -- Los comandos estan dirigidos a windows --
# Para poder iniciar el servidor en Flask
# Se tiene que poner en el cmd set FLASK=APP= 'nombredelarchivo.py'
# Despues ingresar el comando flask run
# Para activar el modo de desarrollador solo se tiene que agregar en el cmd =>
# set FLASK_ENV=development

#Metodos de http
#GET, POST, PUT, PATCH,  DELETE
#PUT se utiliza para reemplazar un recurso
#PATCH para actualizar parcialmente un recurso

#La herramienta curl se utiliza principalmente para transferir datos mediante protocolos
#de internet para la URL determinanada.

#Para acceder a una ruta el comando seria.
#curl -X [metodo http] [ruta]

#Ejemplo:
#curl -X GET localhost:5000/post/1

#Hay 2 maneras para definir los metodos HTTP.
#Separamos las rutas con sus respectivos Metodos
#Ojo. Si se hara de esta manera, cuidado con tener el mismo nombre en la funcion

    # @app.route('/post/<post_id>', methods = [ 'POST'])
    # def lala(post_id):
    #     return 'El id del usuario es:' + ' ' + post_id
    #
    #
    # @app.route('/post/<post_id>', methods = [ 'POST'])
    # def lele(post_id):
    #     return 'El id del usuario es:' + ' ' + post_id

#Tambien se puede agregar los metodos en una misma ruta.

#Usando esta manera, podemos usar el metodo request.method para hacer las validaciones correspondientes.
#NOTA. importar el objeto de request que esta dentro de flask
@app.route('/post/<post_id>', methods = ['GET', 'POST'])
def lala(post_id):
    if request.method == 'GET':
        return 'El id del usuario es por GET:' + ' ' + post_id
    else:
        return 'El id del usuario es por POST:' + ' ' + post_id

# Para nosotros ver los datos que se estan enviando de un formulario, vamos a hacer uso del objeto de request.
# Si nosotros no agregaamos los metodos en las rutas, el metodo por defaul es GET. OJITTO.

# @app.route('/lele', methods=['GET', 'POST'])
# def lele():
#     # print(url_for('index')) #Este metodo es usando para redireccionar a otra url, usando su funcion ya definida
#     # print(url_for('lala', post_id=2)) #En este coso, la funcion pide un parametro, de esta manera se le asgina un valor
#     # print(request.form) # De esta manera obtendremos todos los datos
#     # print(request.form['llave1']) # Ahora, de esta forma obtendremos los datos de la llave1
#     # print(request.form['llave2'])
#
#     abort(403) #Con este metodo, enviara el error dependiendo de cual sea por el navegador para terminar la ejecucion de nuestra aplicacion.
#     return redirect(url_for('lala', post_id=2)) #Esta funcion nos redireccionara a la ruta determinada. PERO OJO.
#     #para hacer que funcionera la redireccion tendremos que agregarle un return,  ya qye de otro caso nos regresa 'lele'
#     return 'lele'

#En alguna ocasiones vamos a abortar nuestras funciones.

#Renderizando plantillas
#Al igual que nosotros podemos regresar documentos HTML nosotros podemos tambine podemos regresar un objeto JSON. Solamente se usa un diccionario
# @app.route('/lele', methods=['GET', 'POST'])
# def lele():
#     # return render_template('lele.html')
#     return {
#         "bellaco": "YayoGO",
#         "ansioso": "yayitocl@hotmail.com"
#     } #Una curiosidad es que se ordena de manera alfabetica.

#Profundizando en el render

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', mensaje = 'Hola mundo')
#Para poder imprimir el mensaje en el documento HTML, solo se tiene que agregar entre '{{}}'
#Ejemplo -> <p> {{mensaje}} </p>


#Conexion a la base de datos

#Instalar el conector de MySQL a Python3 pip3 install mysql-connector-python
#importar mysql
#crear la conexion a la base de datos

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "curso_python"
)

#Agregar nuestro cursor
cursor = db.cursor(dictionary = True) #Con esta condicion nostros habilitamos el uso de los nombre de los campos de las tablas, ya que sin estan
# se tendria que usar el indice para poder obtener los datos

@app.route('/lele', methods=['GET', 'POST'])
def lele():
    cursor.execute('select * from users')
    users = cursor.fetchall()
    print(users)

    return render_template('lele.html', users = users)

#Ingresando registros a la base de datos

@app.route('/crear', methods = ['GET', 'POST'])
def crear():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        sql = 'insert into users (name, surname, password) values (%s, %s, %s)'
        values = (name, surname, password)
        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('lele'))
    return render_template('crear.html')
