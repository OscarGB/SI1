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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

