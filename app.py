from flask import Flask, render_template, request
import pusher
import mysql.connector

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep_tst0_experiencias",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/exp")
def experiencia():
    return render_template("0experiencia.html")

@app.route("/guardar_encuesta", methods=["POST"])
def guardar_encuesta():
    if not con.is_connected():
        con.reconnect()
    
    # Obtener datos del formulario, ya no se incluye el ID de experiencia
    nombre_apellido = request.form["Nombre_Apellido"]
    comentario = request.form["Comentario"]
    calificacion = request.form["Calificacion"]

    cursor = con.cursor()
    sql = "INSERT INTO experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
    val = (nombre_apellido, comentario, calificacion)
    cursor.execute(sql, val)
    
    con.commit()

    # Configuración de Pusher
    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="2df86616075904231311",
        secret="2f91d936fd43d8e85a1a",
        cluster="us2",
        ssl=True
    )

    # Trigger del evento para Pusher
    pusher_client.trigger("registroencusta", "nuevoRegistroEncuesta", {
        "Nombre_Apellido": nombre_apellido,
        "Comentario": comentario,
        "Calificacion": calificacion
    })

    con.close()
    return f"Encuesta guardada: {nombre_apellido} - Calificación: {calificacion}"

@app.route("/buscar_encuestas")
def buscar_encuestas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()

    con.close()

    resultados = [{"Nombre_Apellido": r[1], "Comentario": r[2], "Calificacion": r[3]} for r in registros]

    return resultados

if __name__ == "__main__":
    app.run(debug=True)
