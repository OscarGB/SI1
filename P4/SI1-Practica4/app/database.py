# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # TODO: implementar la consulta; asignar nombre 'cc' al contador resultante
    consulta_preparada = "  PREPARE getListaCliMes (text, int) AS \
                            SELECT COUNT(DISTINCT customerid) as cc\
                            FROM \
                              orders \
                            WHERE\
                              orderdate >= to_date($1, 'YYYYMM') \
                              and orderdate < to_date($1, 'YYYYMM') + interval '1 month'\
                              and totalamount > $2;"

    consulta_no_preparada = "SELECT COUNT(DISTINCT customerid) as cc\
                            FROM \
                              orders \
                            WHERE\
                              orderdate >= to_date('{0}', 'YYYYMM') \
                              and orderdate < to_date('{0}', 'YYYYMM') + interval '1 month'\
                              and totalamount > {1}"
    
    if(use_prepare):
        db_conn.execute(consulta_preparada)
    # TODO: ejecutar la consulta 
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False

    # Array con resultados de la consulta para cada umbral
    dbr=[]

    for ii in range(niter):
        if(use_prepare):
            res = list(db_conn.execute("EXECUTE getListaCliMes ('"+str(anio)+str(mes)+"', "+str(iumbral)+");"))[0]
        else:
            res = list(db_conn.execute(consulta_no_preparada.format(str(anio)+str(mes), str(iumbral))))[0]

        # Guardar resultado de la query
        dbr.append({"umbral":iumbral,"contador":res['cc']})
        if(break0 and res['cc'] == 0): 
            break

        # TODO: si break0 es True, salir si contador resultante es cero
        
        # Actualizacion de umbral
        iumbral = iumbral + iintervalo

    if(use_prepare):
        db_conn.execute("DEALLOCATE getListaCliMes;")
                
    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()  

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}
    
# def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    
#     # Array de trazas a mostrar en la página
#     dbr=[]

#     # TODO: Ejecutar consultas de borrado
#     # - ordenar consultas según se desee provocar un error (bFallo True) o no
#     # - ejecutar commit intermedio si bCommit es True
#     # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
#     # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
#     # - ir guardando trazas mediante dbr.append()
    
#     try:
#         # TODO: ejecutar consultas

#     except Exception as e:
#         # TODO: deshacer en caso de error

#     else:
#         # TODO: confirmar cambios si todo va bien

        
#     return dbr

