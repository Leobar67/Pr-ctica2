from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

# Ruta para guardar la encuesta
@app.route("/guardar_encuesta", methods=["POST"])
def guardar_encuesta():
    try:
        # Verificar que la conexión esté activa
        if not con.is_connected():
            con.reconnect()

        # Obtener los datos del formulario
        Nombre_Apellido = request.form["Nombre_Apellido"]
        Comentario = request.form["Comentario"]
        Calificacion = request.form["Calificacion"]

        cursor = con.cursor()

        # Inserción en la base de datos
        sql = "INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
        val = (Nombre_Apellido, Comentario, Calificacion)
        cursor.execute(sql, val)
        con.commit()

        # Disparar el evento con Pusher para actualizar en tiempo real
        pusher_client = pusher.Pusher(
            app_id="1714541",
            key="2df86616075904231311",
            secret="2f91d936fd43d8e85a1a",
            cluster="us4",
            ssl=True
        )

        pusher_client.trigger("registroencusta", "nuevoRegistroEncuesta", {
            "Nombre_Apellido": Nombre_Apellido,
            "Comentario": Comentario,
            "Calificacion": Calificacion
        })

        # Devolver una respuesta JSON de éxito
        return jsonify({"success": True, "message": "Encuesta guardada exitosamente!"})

    except mysql.connector.Error as err:
        print(f"Error al guardar la encuesta: {err}")
        return jsonify({"success": False, "message": f"Error al guardar la encuesta: {err}"}), 500

# Ruta para buscar encuestas en la base de datos
@app.route("/buscar_encuestas")
def buscar_encuestas():
    try:
        if not con.is_connected():
            con.reconnect()

        cursor = con.cursor()
        cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
        registros = cursor.fetchall()

        resultados = [{"Nombre_Apellido": r[1], "Comentario": r[2], "Calificacion": r[3]} for r in registros]

        return jsonify(resultados)
    
    except mysql.connector.Error as err:
        print(f"Error al buscar encuestas: {err}")
        return jsonify({"success": False, "message": f"Error al buscar encuestas: {err}"})

if __name__ == "__main__":
    app.run(debug=True)
