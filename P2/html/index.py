# -*- coding: utf-8 -*-

from flask import Flask, render_template
from random import shuffle
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
     novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4])

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
    Similares = [a for a in Data["peliculas"] if Peli["categoria"] == a["categoria"]]

    return render_template("pelicula.html",\
     Titulo=pelicula, novedades_sidebar=Novedades[:4], populares_sidebar=Recomendadas[:4],\
     pelicula=Peli, similares=Similares[:8])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

