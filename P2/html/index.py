# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    destacadas = [
    {"nombre":u"Acción", "imagen":"gladiator.jpg"},
    {"nombre":u"Animación", "imagen":"del_reves.jpg"},
    {"nombre":u"Comedia", "imagen":"ocho_apellidos_vascos.jpg"},
    {"nombre":u"Ficción", "imagen":"avatar.jpg"},
    {"nombre":u"Musical", "imagen":"la_la_land.jpg"},
    {"nombre":u"Drama", "imagen":"titanic.jpg"}
    ]
    novedades = [
    {"nombre":u"Indiana Jones", "imagen":"indiana_jones.jpg"},
    {"nombre":u"Indiana Jones 2", "imagen":"indiana_jones2.jpg"},
    {"nombre":u"Campeones", "imagen":"campeones.jpg"},
    {"nombre":u"Lo Imposible", "imagen":"lo_imposible.jpg"},
    {"nombre":u"La La Land", "imagen":"la_la_land.jpg"},
    {"nombre":u"os increibles 2", "imagen":"los_increibles2.jpg"},
    {"nombre":u"Ocho Apellidos Vascos", "imagen":"ocho_apellidos_vascos.jpg"},
    {"nombre":u"Bajo La Misma Estrella", "imagen":"bajo_la_misma_estrella.jpg"},
    {"nombre":u"El gran Showman", "imagen":"el_gran_showman.jpg"},
    {"nombre":u"Del Revés", "imagen":"del_reves.jpg"},
    ]
    return render_template("index.html", destacadas=destacadas, novedades=novedades)

@app.route("/carrito/")
def carrito():
    return render_template("carrito.html")

@app.route("/pagar/")
def pagar():
    return render_template("pagar.html")

@app.route("/contacto/")
def contacto():
    return render_template("contacto.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/user-info/")
def user_info():
    return render_template("user-info.html")

@app.route("/listado_peliculas/")
def listado_peliculas():
    return render_template("listado_peliculas.html")

@app.route("/categorias/")
def categorias():
    return render_template("categorias.html")

@app.route("/categorias/<categoria>/")
def categorias_categoria(categoria):
    return render_template("categoria.html", Titulo=categoria)

@app.route("/peliculas/<pelicula>/")
def pelicula(pelicula):
    return render_template("pelicula.html", Titulo=pelicula)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

