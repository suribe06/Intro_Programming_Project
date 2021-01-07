from flask import *
from flask_socketio import *
import time, json, requests, os

#Configuramos la app
app = Flask(__name__)
app.debug = True
app.config.update(DEBUG = True, SECRET_KEY = '696969', USERNAME='Admin', PASSWORD='23ll')
io = SocketIO(app)
namespace = "/fsic"


@io.on("connect", namespace=namespace)
def conectar():
    print("El cliente esta conectado")


@io.on("disconnect", namespace=namespace)
def desconectar():
    print("El cliente esta desconectado")

@io.on("new-message", namespace=namespace)
def nuevo_mensaje(message):
    print("Ha llegado un nuevo mensaje {!r}".format(message))

    io.emit("new-message", message, namespace=namespace)

@io.on("new-message-individual", namespace=namespace)
def nuevo_mensaje_individual(message):
    contenido = message[0]
    usuario = message[1]
    contactos = message[2]
    fecha_hora = time.strftime("%c")
    pais = requests.get('http://ip-api.com/json/').json().get("country")
    archivo = "conversaciones/" + usuario + "-" + "-".join(contactos) + ".txt"

    fp = open(archivo, "a")
    mensaje_archivo = "{contenido} ({usuario}, {fecha_hora}, {pais})\n".format(
        contenido=contenido,
        usuario=usuario,
        fecha_hora=fecha_hora,
        pais=pais)
    fp.write(mensaje_archivo)
    fp.close()

    for contacto in contactos:
        respuesta = {
            'destino': contacto,
            'fuente': usuario,
            'contenido': contenido,
            'fecha': fecha_hora,
            'lugar': pais
        }

        io.emit("message-individual", respuesta, namespace=namespace)

@io.on("contacto-seleccionado", namespace=namespace)
def contacto_seleccionado(message):
    usuario = message[0]
    contactos = message[1]
    archivo = "conversaciones/" + usuario + "-" + "-".join(contactos) + ".txt"

    contenido = ""
    if os.path.exists(archivo):
    	fp = open(archivo, "r")
    	contenido = fp.read()
    	fp.close()

    for contacto in contactos:
        respuesta = {
            'destino': contacto,
            'fuente': usuario,
            'contenido': contenido
        }

        io.emit("contacto-seleccionado", respuesta, namespace=namespace)

@app.route('/', methods=['GET', 'POST'])

def login():
	"""
	Esta funcion recoge los datos introducidos para el inicio de sesion y procede a la aplicacion si el usuario se encuentra registrado.
	"""
	if(request.method == 'POST'):
		n = request.form['nombre']
		c = request.form['contrasena']
		lista_usuarios = []
		lista_contrasenas = []
		session['user']=request.form['nombre'] 

		f = open("usuarios.txt", "r")
		for texto in f.readlines():
			texto = texto.strip()
			if(texto and texto not in lista_usuarios):
				lista_usuarios.append(texto)
		f.close()

		f2 = open("contrasenas.txt", "r")
		for texto2 in f2.readlines():
			texto2 = texto2.strip()
			if(texto2 and texto2 not in lista_contrasenas):
				lista_contrasenas.append(texto2)
		f2.close()

		if(n in lista_usuarios):
			if(c in lista_contrasenas):
				if(lista_usuarios.index(n) == lista_contrasenas.index(c)):
					con = open("conectados.txt", "r")
					tex = con.readlines()
					con.close()
					con = open("conectados.txt", "a")
					con.write("\n" + str(n))
					con.close()


					return redirect(url_for("chat"))
				else:
					return render_template('denegado.html')
			else:
				return render_template('denegado.html')
		else:
			return render_template('register.html')
	return render_template('home.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def registrarse():
	"""
	Esta funcion agrega los datos del registro a los archivos de usuarios y contrasenas
	"""
	if(request.method == 'POST'):
		n = request.form['new_nombre']
		c1 = request.form['new_contrasena']
		c2 = request.form['conf_contrasena']
		lista_usuarios = []
		lista_contrasenas = []
		if(c1 == c2):
			file = open("Contactos_Usuarios/" + str(n) + ".txt", "w")
			file.close()
			lista_usuarios.append(n)
			lista_contrasenas.append(c1)
			def archivos():
				u = open("usuarios.txt","r")
				texto = u.readlines()
				u.close()
				u = open("usuarios.txt", "a")
				u.write("\n" + str(n))
				u.close()

				c = open("contrasenas.txt", "r")
				texto2 = c.readlines()
				c.close()
				c = open("contrasenas.txt", "a")
				c.write("\n" + str(c1))
				c.close()

			archivos()
			return render_template('home.html')
		else:
			return render_template('denegado.html')
	return render_template('register.html')


"""def guardarimagen(imagen):
	image = open("imagenes/" + str(usuario) + ".jpg", "wb")
	r = imagen.readlines()
	s = b''
	s = s + b''.join(r)
	image.write(s)
	image.close()"""


@app.route('/mainpage', methods=['GET', 'POST'])
def chat():
	"""
	Esta funcion contiene todas las funciones que se pueden realizar en la pagina del chat
	"""
	usuario = None
	if 'user' in session:
		mensaje = ""
		usuario = session['user']
		if(request.method == 'POST'):
			"""if(request.form['btn'] == "enviar"): 
				guardarimagen(request.form['archivo'])"""

			if(request.form['btn'] == "Salir"):
				session.pop('user', None)
				ll = []
				f = open("conectados.txt", "r")
				for linea in f.readlines():
					linea = linea.strip()
					if(linea and linea not in ll):
						ll.append(linea)
				f.close()
				ll.remove(usuario)
				f = open("conectados.txt", "w")
				for i in ll:
					f.write("\n" + i)
				f.close()

			if(request.form['btn'] == "agregar"):
				nom = session['user']
				u = request.form['agregar']
				lista_usuarios = []
				f = open("usuarios.txt", "r")
				for texto in f.readlines():
					texto = texto.strip()
					if(texto and texto not in lista_usuarios):
						lista_usuarios.append(texto)
				f.close()
				
				if(u in lista_usuarios):
					file = open("Contactos_Usuarios/" + str(nom) + ".txt", "a")
					file.write("\n"+ u)
					file.close()
				else:
					mensaje = "El usuario ingresado no existe"
		
		llc = []
		sup = open("conectados.txt", "r")
		for linea in sup.readlines():
			linea = linea.strip()
			if(linea and linea not in llc):
				llc.append(linea)
		sup.close()
		print(llc)
	
		lista = []
		x = "en linea"
		y = "desconectado"
		if(usuario):
			file = open("Contactos_Usuarios/" + str(usuario) + ".txt", "r")
			for contacto in file.readlines():
				contacto = contacto.strip()
				if(contacto and contacto not in lista):
					lista.append(contacto)
			file.close()
			lista_mensajes = []

		return render_template('mainpage.html', mensaje=mensaje, usuario=usuario, lista=lista, llc=llc, x=x, y=y, lista_mensajes=lista_mensajes)
	else:
		return redirect(url_for('login'))

if __name__ == "__main__":
	io.run(app)