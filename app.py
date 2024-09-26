from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id="1714541",
    key="2df86616075904231311",
    secret="2f91d936fd43d8e85a1a",
    cluster="us2",
    ssl=True
)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/exp")
def experiencia():
    return render_template("0experiencia.html")

# Ruta para guardar la encuesta
@app.route("/guardar_encuesta", methods=["POST"])
def guardar_encuesta():
    if not con.is_connected():
        con.reconnect()

    # Obtener datos del formulario
    id_experiencia = request.form["Id_Experiencia"]
    nombre_apellido = request.form["Nombre_Apellido"]
    comentario = request.form["Comentario"]
    calificacion = request.form["Calificacion"]

    cursor = con.cursor()
    sql = "INSERT INTO experiencias (Id_Experiencia, Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s, %s)"
    val = (id_experiencia, nombre_apellido, comentario, calificacion)
    cursor.execute(sql, val)
    con.commit()

    # Trigger del evento para Pusher
    pusher_client.trigger("registroencuesta", "nuevoRegistroEncuesta", {
        "Id_Experiencia": id_experiencia,
        "Nombre_Apellido": nombre_apellido,
        "Comentario": comentario,
        "Calificacion": calificacion
    })

    return f"Encuesta guardada: {nombre_apellido} - Calificación: {calificacion}"

# Ruta para buscar encuestas
@app.route("/buscar_encuestas", methods=["GET"])
def buscar_encuestas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()

    resultados = [{"Id_Experiencia": r[0], "Nombre_Apellido": r[1], "Comentario": r[2], "Calificacion": r[3]} for r in registros]

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=True)
