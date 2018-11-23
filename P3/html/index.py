# -*- coding: utf-8 -*-

#Imports
from flask import Flask, render_template, request, session
from random import shuffle, randint
from urlparse import urlparse
from hashlib import md5
import time
import json, os, re
from sqlalchemy import create_engine, update
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, and_, insert
from sqlalchemy.sql.expression import func

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
# cargar las tablas desde una base de datos existente
db_meta = MetaData(bind=db_engine, reflect = True)
# conexion a la base de datos
db_conn = db_engine.connect()

non_decimal = re.compile(r'[^\d.]+')

#Flask App
app = Flask(__name__)

#Secret Key for cookie encryption
app.secret_key = 'esto-es-una-clave-muy-secreta'

productos = db_meta.tables['productos']
peliculas = db_meta.tables['peliculas']
result = list(db_conn.execute("SELECT * FROM peliculas natural join productos where stock > 0;"))
Data = []
for a in result:
    auxdic = {"productoid":a[3], "titulo":a[1], "precio":a[4], "poster":"la_mascara.jpg"}
    Data.append(auxdic)

#Conseguir todas los generos
generos = db_meta.tables['generos']
query = select([generos])
result = list(db_conn.execute(query))
Categorias = []
for a in result:
    auxdic = {"categoriaid": a[0], "nombre": a[1], "imagen":"la_mascara.jpg"}
    Categorias.append(auxdic)
    
#Ordenar las peliculas por año (las mas nuevas primero)
result = list(db_conn.execute("SELECT * FROM peliculas natural join productos where stock > 0 ORDER BY estreno LIMIT 10;"))
Novedades=[]
for a in result:
    auxdic = {"titulo": a[1], "poster":"la_mascara.jpg", "peliculaid":a[0], "productoid":a[3]}
    Novedades.append(auxdic)

def getPelicula(pelicula):
    result = list(db_conn.execute("SELECT * FROM (SELECT* FROM productos where productoid = "+str(pelicula)+" and stock > 0) AS T1 natural join peliculas;"))[0]
    pelicula = {"peliculaid":result[0], "productoid":result[1], "titulo": result[6], "poster": "la_mascara.jpg", "precio":result[2], "anno":result[7]}
    pelicula["paises"] = []
    result = list(db_conn.execute("SELECT * FROM (SELECT* FROM peliculas where peliculaid = "+str(pelicula["peliculaid"]) +") AS T1 natural join paispeliculas natural join paises;"))
    for a in result:
        pelicula["paises"].append(a[4])
    pelicula["actores"] = []
    result = list(db_conn.execute("SELECT * FROM (SELECT* FROM peliculas where peliculaid = "+str(pelicula["peliculaid"]) +") AS T1 natural join actorpeliculas natural join actores LIMIT 10;"))
    for a in result:
        pelicula["actores"].append(a[6])
    result = list(db_conn.execute("SELECT * FROM (SELECT* FROM peliculas where peliculaid = "+str(pelicula["peliculaid"]) +") AS T1 natural join directorpeliculas natural join directores;"))
    if(len(result) > 0):
        pelicula["director"] = result[0][4]
    
    return pelicula

def getSimilares(Peli):
    result = list(db_conn.execute("SELECT * FROM (SELECT* FROM peliculas where peliculaid = "+str(Peli["peliculaid"]) +") AS T1 natural join generopeliculas natural join generos;"))[0]
    return get_pelis_en_categoria(result[0])[:10]

def get_pelis_en_categoria(categoria):
    result = list(db_conn.execute("SELECT * FROM (SELECT * FROM generopeliculas where generoid="+str(categoria)+") AS T1 natural join peliculas natural join productos  where stock > 0;"))
    peliscat = []
    for a in result:
        auxdic = {"productoid":a[4], "titulo":a[2], "precio":a[5], "poster":"la_mascara.jpg"}
        peliscat.append(auxdic)
    return peliscat

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
    if categoria is not None:
        result = list(db_conn.execute("SELECT * FROM (SELECT * FROM peliculas where titulo like '%%"+str(name)+"%%') as T natural join productos natural join generopeliculas where generoid = "+str(categoria)+";"))
        peliscat = []
        for a in result:
            auxdic = {"productoid":a[3], "titulo":a[1], "precio":a[4], "poster":"la_mascara.jpg"}
            peliscat.append(auxdic)
        return peliscat
    result = list(db_conn.execute("SELECT * FROM (SELECT * FROM peliculas where titulo like '%%"+str(name)+"%%') as T natural join productos;"))
    peliscat = []
    for a in result:
        auxdic = {"productoid":a[3], "titulo":a[1], "precio":a[4], "poster":"la_mascara.jpg"}
        peliscat.append(auxdic)
    return peliscat

def check_password(email, password):
    try:
        clientes = db_meta.tables['clientes']
        query = select([clientes]).where(and_(clientes.c.email == email, clientes.c.password == password))
        result = db_conn.execute(query)
        a = list(result)[0]
        iduser = a[0]
        saldo = a[2]
        useremail = a[3]
        nombre = a[4]
        session["userid"] = iduser
        session["user"] = nombre
        session["email"] = useremail
        session["saldo"] = saldo
        result = list(db_conn.execute("SELECT SUM(cantidad) FROM (select * from pedidos where clienteid = "+str(iduser)+" and estado is null order by fecha DESC) as T inner join detallespedidos on T.pedidoid = detallespedidos.pedidoid"))
        if(len(result) == 0):
            ncompra = 0
        else:
            ncompra = result[0][0]

        # Cargar carrito de antes de hacer login
        if "ncompra" in session:
            ncompra += session["ncompra"]
            session.pop("ncompra", None)
            for a in session["compra"]:
                anadir_al_carrito(a)
            session.pop("compra", None)
        if(ncompra == 0):
            session.pop("ncompra", None)
        else:
            session["ncompra"] = ncompra


        return True
    except Exception as e:
        return False


def create_user_and_login(user, pwd, email, card, path):
    try:
        clientes = db_meta.tables['clientes']
        query = select([func.max(clientes.c.clienteid)])
        result = db_conn.execute(query)
        maxid = list(result)[0][0]
        query = clientes.insert().values(clienteid=maxid+1, tarjeta=card, saldo=randint(1,100), email=email, nombre=user, password=pwd)
        result = db_conn.execute(query)
        return check_password(email, pwd)
    except Exception as e:
        return False

def change_saldo():
    clientes = db_meta.tables['clientes']
    query = update(clientes).where(clientes.c.clienteid == session["userid"]).values(saldo=session["saldo"])
    db_conn.execute(query)

def recarga_saldo():
    db_conn.execute("UPDATE clientes SET saldo = saldo + 100 WHERE clienteid = "+str(session["userid"])+";")
    session["saldo"] += 100

def get_historial():
    result = list(db_conn.execute("select * from pedidos where clienteid = "+str(session["userid"])+" and estado is not null order by fecha DESC;"))
    if(len(result) == 0):
        return None
    historial = []
    for a in result:
        auxdic = {"pedidoid":a[0], "fecha":a[1], "precio":round(a[5],2), "estado":a[6], "peliculas":[]}
        result2 = list(db_conn.execute("SELECT * from (select * from detallespedidos where pedidoid = "+str(auxdic["pedidoid"])+") as T natural join productos natural join peliculas;"))
        for b in result2:
            auxdic2 = {"titulo": b[9], "precio": round(b[3],2), "cantidad": b[4], "poster": "la_mascara.jpg"}
            auxdic["peliculas"].append(auxdic2)
        historial.append(auxdic)
    return historial

@app.route("/")
def index():
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("index.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     destacadas=Categorias[:6], categorias=Categorias, novedades=Novedades[:10], user=user)

def getcarrito():
    if "user" in session:        
        result = list(db_conn.execute("select * from pedidos where clienteid = "+str(session["userid"])+" and estado is null;"))
        if(len(result) == 0):
            return 0,None
        pedidoid = result[0][0]
        precioneto = result[0][3]
        result = list(db_conn.execute("SELECT * from (select * from detallespedidos where pedidoid = "+str(pedidoid)+") as T natural join productos natural join peliculas;"))
        if(len(result) == 0):
            return 0,None
        else:
            compradas = []
            for b in result:
                auxdic = {"titulo": b[9], "precio": round(b[3],2), "cantidad": b[4], "poster": "la_mascara.jpg", "productoid":b[1]}
                compradas.append(auxdic)
        return precioneto, compradas


    else:
        if "ncompra" in session:
            done = []
            compradas = []
            precioneto = 0
            for a in session["compra"]:
                if a in done:
                    continue
                done.append(a)
                b = list(db_conn.execute("SELECT * from (select * from productos where productoid = "+str(a)+") as T natural join peliculas;"))[0]
                auxdic = {"titulo": b[6], "precio": round(b[2],2), "cantidad": session["compra"].count(a), "poster": "la_mascara.jpg", "productoid":b[1]}
                precioneto += auxdic["precio"]*auxdic["cantidad"]
                compradas.append(auxdic)
            return precioneto, compradas
        else:
            return 0, None

@app.route("/carrito/")
def carrito():
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    suma, compra = getcarrito()
    return render_template("carrito.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     user=user, compradas=compra, total=suma)

@app.route("/carrito/<valor>/modificar/", methods=["POST"])
def carrito_modificar(valor):
    if "user" in session:
        user = session["userid"]
        if "ncompra" in session:
            nueva_can = request.form["cantidad"]
            result = list(db_conn.execute("select * from pedidos where clienteid = "+str(session["userid"])+" and estado is null;"))
            if(len(result) == 0):
                return
            pedidoid = result[0][0]
            result = list(db_conn.execute("select * from detallespedidos where pedidoid = "+str(pedidoid)+" and productoid = "+str(valor)+";"))
            if(len(result) > 0):
                precioproducto = result[0][2]/result[0][3] 
                session["ncompra"] += int(nueva_can)-result[0][3]
                db_conn.execute("UPDATE detallespedidos SET cantidad = "+str(nueva_can)+", preciototal = "+str(int(nueva_can)*precioproducto)+" where pedidoid = "+str(pedidoid)+" and productoid = "+str(valor)+";")
            else:
                return
    else:
        user = None
        if "ncompra" in session:
            nueva_can = request.form["cantidad"]
            vieja_can = session["compra"].count(valor)
            session["ncompra"] += (int(nueva_can) - int(vieja_can))
            for a in range(int(nueva_can) - int(vieja_can)):
                session["compra"].append(valor)
            for a in range(int(vieja_can) - int(nueva_can)):
                session["compra"].delete(valor)
            if(session["ncompra"] <= 0):
                session.pop("ncompra", None)
                session.pop("compra", None)

    return carrito()

def remove_from_carrito(valor):
    if "user" in session:
        result = list(db_conn.execute("select * from pedidos where clienteid = "+str(session["userid"])+" and estado is null;"))
        if(len(result) == 0):
            return
        pedidoid = result[0][0]
        result = list(db_conn.execute("select * from detallespedidos where pedidoid = "+str(pedidoid)+" and productoid = "+str(valor)+";"))
        if(len(result) > 0):
            session["ncompra"] -= result[0][3]
            db_conn.execute("DELETE from detallespedidos where pedidoid = "+str(pedidoid)+" and productoid = "+str(valor)+";")
        else:
            return

    else:
        session["ncompra"] -= session["compra"].count(valor)
        session["compra"] = filter(lambda a: a != valor, session["compra"])

@app.route("/carrito/<valor>/borrar/")
def carrito_borrar(valor):
    remove_from_carrito(valor)
    return carrito()

@app.route("/pagar/")
def pagar():
    if "user" in session:
        user = session["userid"]
    else:
        return login()
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    suma, compra = getcarrito()
    return render_template("pagar.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     user=user, total=suma)

def finalizar_pedido():
    result = list(db_conn.execute("select * from pedidos where clienteid = "+str(session["userid"])+" and estado is null;"))
    if(len(result) == 0):
        return
    pedidoid = result[0][0]
    db_conn.execute("update pedidos set estado='Paid', fecha=NOW() where pedidoid = "+str(pedidoid)+";")


@app.route("/pagar/confirmar/", methods=["POST"])
def pagar_1():
    if "user" in session:
        user = session["userid"]
    else:
        return login()
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    suma, compra = getcarrito()

    if suma > session["saldo"]:
        return render_template("pagar.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     user=user, total=suma, error=1)
    else:
        session["saldo"] -= float(suma)
        change_saldo()
        finalizar_pedido()
        session.pop("ncompra", None)
        session.pop("compra", None)
    return index()

@app.route("/contacto/")
def contacto():
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("contacto.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     user=user)

@app.route("/login/")
def login():
    if "user" in session:
        return index()
    else:
        user = None
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("login.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     user=user)

@app.route("/login/activate/", methods=['POST'])
def login_fun():
    if "user" in session:
        return index()
    user = request.form["user"]
    pwd = request.form["password"]
    if(check_password(user, pwd)):
        return index()
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("login.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     wrong=True)

@app.route("/register/")
def register():
    if "user" in session:
        return index()
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("register.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra)

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
        if "ncompra" in session:
            ncompra = session["ncompra"]
        else:
            ncompra = 0
        return render_template("register.html",\
         novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
         error=True)
    create_user_and_login(user, pwd, email, card, path)
    return index()

@app.route("/users/<userc>/")
def user_info(userc):
    if "user" in session:
        user = session["userid"]
        username = session["user"]
        email = session["email"]
        saldo = session["saldo"]
        historial = get_historial()[:5]
        if userc != str(session["userid"]):
           return index()
    else:
        return index()
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("user-info.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     user=user, username=username, email=email, saldo=saldo, historial=historial)

@app.route("/contador/")
def contador():
    return str(randint(1,99))

@app.route("/user_exists/<userc>/")
def user_exists(userc):
    path = os.path.dirname(__file__)+ "/usuarios/"+userc+"/datos.dat"
    if(os.path.exists(path)):
        return "True"
    else :
        return "False"

@app.route("/recargar/<userc>/")
def recargar(userc):
    if "user" in session:
        user = session["userid"]
        recarga_saldo()
    return user_info(userc)

@app.route("/listado_peliculas/<i>")
def listado_peliculas(i):
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    i = int(i)
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("listado_peliculas.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     peliculas = Data[12*(i-1):12*i], user=user, i=i)

@app.route("/categorias/")
def categorias():
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("categorias.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     categorias=Categorias, user=user)

@app.route("/categorias/<categoria>/<i>/")
def categorias_categoria(categoria, i):
    for a in Categorias:
        if str(a["categoriaid"]) == categoria:
            nombre = a["nombre"]
            break
    i = int(i)
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("categoria.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     Titulo=nombre, i=i, categoriaid=categoria, peliculas=get_pelis_en_categoria(categoria)[12*(i-1):12*i], user=user)

@app.route("/peliculas/<pelicula>/")
def pelicula(pelicula):
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    Peli = getPelicula(pelicula)
    Similares = getSimilares(Peli)
    shuffle(Similares)

    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("pelicula.html",\
     Titulo=Peli["titulo"], novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     pelicula=Peli, similares=Similares[:8], user=user)

def anadir_al_carrito(productoid):
    if "user" in session:
        user = session["userid"]
        if "ncompra" in session:
            session["ncompra"] += 1
        else:
            session["ncompra"] = 1

        result = list(db_conn.execute("select * from pedidos where clienteid = "+str(session["userid"])+" and estado is null;"))
        if(len(result) == 0):
            db_conn.execute("INSERT INTO pedidos VALUES ((select MAX(pedidoid) from pedidos) + 1, NOW(), "+str(session["userid"])+", 0, 15, 15, NULL);")
            result = list(db_conn.execute("select * from pedidos where clienteid = "+str(session["userid"])+" and estado is null;"))
        
        pedidoid = result[0][0]
        result = list(db_conn.execute("select * from detallespedidos where pedidoid = "+str(pedidoid)+" and productoid = "+str(productoid)+";"))
        if(len(result) > 0):
            db_conn.execute("UPDATE detallespedidos\
            SET cantidad = cantidad + 1,\
                preciototal = (preciototal/cantidad)*(cantidad+1)\
            WHERE pedidoid = "+str(pedidoid)+" and productoid = "+str(productoid)+";")
        else:
            db_conn.execute("INSERT INTO detallespedidos VALUES\
            ("+str(pedidoid)+", "+str(productoid)+", (SELECT precio from productos where productoid = "+str(productoid)+"),1)")
    else:
        if "ncompra" in session:
            session["ncompra"] += 1
            session["compra"].append(productoid)
        else:
            session["ncompra"] = 1
            session["compra"] = [productoid, ]

@app.route("/peliculas/<productoid>/comprar/")
def comprar(productoid):

    anadir_al_carrito(productoid)
    
    return pelicula(productoid)

@app.route("/busqueda/")
def busqueda():
    if "user" in session:
        user = session["userid"]
    else:
        user = None
    nombre = request.args.get('search')
    categoria = request.args.get('categoria')
    if categoria == '0':
        categoria = None
    if "ncompra" in session:
        ncompra = session["ncompra"]
    else:
        ncompra = 0
    return render_template("busqueda.html",\
     novedades_sidebar=Novedades[:4], populares_sidebar=Novedades[:4], ncompra=ncompra,\
     peliculas=get_pelis_by_name(nombre, categoria), nombre=nombre, categoria=categoria,\
     user=user)

@app.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("ncompra", None)
    session.pop("compra", None)
    session.pop("userid", None)
    return index()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

