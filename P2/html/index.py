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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

