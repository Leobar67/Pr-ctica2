from flask import Flask

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()

    return render_template("experiencias.html")

# Ejemplo de ruta GET usando templates para mostrar una vista
@app.route("/experiencias")
def experiencias():
    con.close()

    return render_template("experiencias.html")

# Ejemplo de ruta POST para ver cómo se envia la informacion
@app.route("/experiencias/guardar", methods=["POST"])
def experienciasGuardar():
    con.close()
    nombreapellido = request.form["txtNombreApellido"]
    comentario = request.form["txtComentario"]
    calificacion = request.form["txtCalificacion"]

    return f"Nombre y Apellido {nombreapellido} Comentario {comentario} Calificacion {calificacion}"

# Código usado en las prácticas
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()

    con.close()

    return registros

@app.route("/experiencias/guardar", methods=["GET"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    sql = "INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
    cursor.execute(sql)
    
    con.commit()
    con.close()

    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="2df86616075904231311",
        secret="2f91d936fd43d8e85a1a",
        cluster="us2",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosexperiencias", "registroexperiencias", args)

    return args
