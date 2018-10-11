# -*- coding: utf-8 -*-

#Imports
from flask import Flask, render_template, request, session
from random import shuffle, randint
from urlparse import urlparse
from hashlib import md5
import json,os

#Flask App
app = Flask(__name__)

#Secret Key for cookie encryption
app.secret_key = 'esto-es-una-clave-muy-secreta'

#Datos del catalogo (Data es un diccionario)
Data = open(os.path.dirname(__file__)+"/catalogo.json", "r").read()
Data = json.loads(Data)

#Conseguir todas las categorias, sin repetidos
aux = list(set([a["categoria"] for a in Data["peliculas"]]))
Categorias = []
for a in aux:
    auxdic = {"nombre": a, "imagen": None}
    for film in Data["peliculas"]:
        if (film["categoria"] == a):
            auxdic["imagen"] = film["poster"]
            break
    Categorias.append(auxdic)

#Ordenar las peliculas por año (las mas nuevas primero)
Novedades = sorted(Data["peliculas"], key=lambda x: -int(x["anno"]))

#Obtener las peliculas ordenadas por puntuacion de los criticos
def sort_rec(x):
    aux = 0.0
    for a in x["opiniones"]:
        aux += float(a["puntuacion"])
    return -aux/len(x["opiniones"])
Recomendadas = sorted(Data["peliculas"], key=lambda x: sort_rec(x))

def get_pelis_en_categoria(categoria):
    return [a for a in Data["peliculas"] if (categoria == a["categoria"])]

#Elimina acentos y eñes (para busquedas)
def normalize(s):
    replacements = (
        (u"á", u"a"),
        (u"é", u"e"),
        (u"í", u"i"),
        (u"ó", u"o"),
        (u"ú", u"u"),
        (u"ñ", u"n")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s.lower()

def get_pelis_by_name(name, categoria):
    if categoria is None:
        return [a for a in Data["peliculas"] if (normalize(name) in normalize(a["titulo"]))]
    return [a for a in Data["peliculas"] if (normalize(name) in normalize(a["titulo"]) and categoria == a["categoria"])]

def check_password(path,password):
    user_data = open(path, "r").read()
    user_data = json.loads(user_data)
    m = md5()
    m.update(password)
    password = m.hexdigest()
    if(user_data["contrasena"] == password):
        session["user"] = user_data["usuario"]
        session["email"] = user_data["email"]
        session["saldo"] = user_data["saldo"]
        return True
    return False

def create_user_and_login(user, pwd, email, card, path):
    m = md5()
    m.update(pwd)
    password = m.hexdigest()
    os.mkdir(path)
    dic={"contrasena": password,\
        "email": email,\
        "usuario": user,\
        "tarjeta": card,\
        "saldo": randint(0,100)}
    open(path+"datos.dat", "w").write(json.dumps(dic))
    session["user"] = dic["usuario"]
    session["email"] = dic["email"]
    session["saldo"] = dic["saldo"]


@app.route("/")
def index():
    if "user" in session:
        user = session["user"]
    else:
        user = None
    return render_template("index.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     destacadas=Categorias, novedades=Novedades[:10], user=user)

@app.route("/carrito/")
def carrito():
    if "user" in session:
        user = session["user"]
    else:
        user = None
    return render_template("carrito.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     user=user)

@app.route("/pagar/")
def pagar():
    if "user" in session:
        user = session["user"]
    else:
        user = None
    return render_template("pagar.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     user=user)

@app.route("/contacto/")
def contacto():
    if "user" in session:
        user = session["user"]
    else:
        user = None
    return render_template("contacto.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     user=user)

@app.route("/login/")
def login():
    if "user" in session:
        return index()
    else:
        user = None
    return render_template("login.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     user=user)

@app.route("/login/activate/", methods=['POST'])
def login_fun():
    if "user" in session:
        return index()
    user = request.form["user"]
    pwd = request.form["password"]
    path = os.path.dirname(__file__)+ "/usuarios/"+user+"/datos.dat"
    if(os.path.exists(path)):
        if(check_password(path, pwd)):
            return index()
    return render_template("login.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     wrong=True)

@app.route("/register/")
def register():
    if "user" in session:
        return index()
    return render_template("register.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/register/activate/", methods=['POST'])
def register_fun():
    if "user" in session:
        return index()
    user = request.form["user"]
    pwd = request.form["passwd"]
    email = request.form["email"]
    card = request.form["card"]
    path = os.path.dirname(__file__)+ "/usuarios/"+user+"/"
    if(os.path.exists(path)):
        return render_template("register.html",\
         novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
         error=True)
    create_user_and_login(user, pwd, email, card, path)
    return index()

@app.route("/users/<userc>/")
def user_info(userc):
    if "user" in session:
        user = session["user"]
        email = session["email"]
        saldo = session["saldo"]
        if userc != user:
            return index()
    else:
        return index()
    return render_template("user-info.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     user=user, email=email, saldo=saldo)

@app.route("/listado_peliculas/<i>")
def listado_peliculas(i):
    if "user" in session:
        user = session["user"]
    else:
        user = None
    i = int(i)
    return render_template("listado_peliculas.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     peliculas = Data["peliculas"][12*(i-1):12*i], user=user, i=i)

@app.route("/categorias/")
def categorias():
    if "user" in session:
        user = session["user"]
    else:
        user = None
    return render_template("categorias.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     categorias=Categorias, user=user)

@app.route("/categorias/<categoria>/")
def categorias_categoria(categoria):
    if "user" in session:
        user = session["user"]
    else:
        user = None
    return render_template("categoria.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     Titulo=categoria, peliculas=get_pelis_en_categoria(categoria), user=user)

@app.route("/peliculas/<pelicula>/")
def pelicula(pelicula):
    if "user" in session:
        user = session["user"]
    else:
        user = None
    Peli = [a for a in Data["peliculas"] if a["titulo"] == pelicula][0]
    Similares = [a for a in get_pelis_en_categoria(Peli["categoria"]) if (Peli["titulo"] != a["titulo"])]
    shuffle(Similares)

    return render_template("pelicula.html",\
     Titulo=pelicula, novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     pelicula=Peli, similares=Similares[:8], user=user)

@app.route("/busqueda/")
def busqueda():
    if "user" in session:
        user = session["user"]
    else:
        user = None
    nombre = request.args.get('search')
    categoria = request.args.get('categoria')
    if categoria == '0':
        categoria = None
    return render_template("busqueda.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     peliculas=get_pelis_by_name(nombre, categoria), nombre=nombre, categoria=categoria,\
     user=user)

@app.route("/logout/")
def logout():
    session.pop("user", None)
    return index()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

