# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from random import shuffle
from urlparse import urlparse
import json,os



Data = open(os.path.dirname(__file__)+"/peliculas.json", "r").read()
Data = json.loads(Data)

aux = list(set([a["categoria"] for a in Data["peliculas"]]))
Categorias = []
for a in aux:
    auxdic = {"nombre": a, "imagen": None}
    for film in Data["peliculas"]:
        if (film["categoria"] == a):
            auxdic["imagen"] = film["poster"]
            break
    Categorias.append(auxdic)

Novedades = sorted(Data["peliculas"], key=lambda x: -int(x["anno"]))

def sort_rec(x):
    aux = 0.0
    for a in x["opiniones"]:
        aux += float(a["puntuacion"])
    return -aux/len(x["opiniones"])
Recomendadas = sorted(Data["peliculas"], key=lambda x: sort_rec(x))

def get_pelis_en_categoria(categoria):
    return [a for a in Data["peliculas"] if (categoria == a["categoria"])]

def get_pelis_by_name(name, categoria):
    if categoria is None:
        return [a for a in Data["peliculas"] if (name in a["titulo"])]
    return [a for a in Data["peliculas"] if (name in a["titulo"] and categoria == a["categoria"])]

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     destacadas=Categorias, novedades=Novedades[:10])

@app.route("/carrito/")
def carrito():
    return render_template("carrito.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/pagar/")
def pagar():
    return render_template("pagar.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/contacto/")
def contacto():
    return render_template("contacto.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/login/")
def login():
    return render_template("login.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/register/")
def register():
    return render_template("register.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/user-info/")
def user_info():
    return render_template("user-info.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/listado_peliculas/")
def listado_peliculas():
    return render_template("listado_peliculas.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     peliculas = Data["peliculas"])

@app.route("/categorias/")
def categorias():
    return render_template("categorias.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/categorias/<categoria>/")
def categorias_categoria(categoria):
    return render_template("categoria.html",\
     Titulo=categoria, novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

@app.route("/peliculas/<pelicula>/")
def pelicula(pelicula):
    Peli = [a for a in Data["peliculas"] if a["titulo"] == pelicula][0]
    Similares = [a for a in get_pelis_en_categoria(Peli["categoria"]) if (Peli["titulo"] != a["titulo"])]
    shuffle(Similares)

    return render_template("pelicula.html",\
     Titulo=pelicula, novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     pelicula=Peli, similares=Similares[:8])

@app.route("/busqueda/")
def busqueda():
    nombre = request.args.get('search')
    categoria = request.args.get('categoria')
    if categoria == '0':
        categoria = None
    return render_template("busqueda.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     peliculas=get_pelis_by_name(nombre, categoria), nombre=nombre, categoria=categoria)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

