from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

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

