from flask import Flask, render_template, request
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
    return render_template("app.html")

# Ruta para guardar la encuesta
@app.route("/guardar_encuesta", methods=["POST"])
def guardar_encuesta():
    print(request.form)
    try:
        # Revisa si la conexión sigue activa
        if not con.is_connected():
            con.reconnect()

        Nombre_Apellido = request.form["Nombre_Apellido"]
        Comentario = request.form["Comentario"]
        Calificacion = request.form["Calificacion"]

        cursor = con.cursor()

        # Imprime la consulta SQL para verificar que esté construida correctamente
        sql = "INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
        val = (Nombre_Apellido, Comentario, Calificacion)
        print(f"Consulta SQL: {sql} con valores {val}")

        cursor.execute(sql, val)
        con.commit()

        print(f"Inserción exitosa para {Nombre_Apellido}")

        pusher_client = pusher.Pusher(
            app_id="1714541",
            key="2df86616075904231311",
            secret="2f91d936fd43d8e85a1a",
            cluster="us3",
            ssl=True
        )

        pusher_client.trigger("registroencusta", "nuevoRegistroEncuesta", {
            "Nombre_Apellido": Nombre_Apellido,
            "Comentario": Comentario,
            "Calificacion": Calificacion
        })

        return f"Encuesta guardada: {Nombre_Apellido} - Calificación: {Calificacion}"
    
    except mysql.connector.Error as err:
        # Imprime el error SQL específico
        print(f"Error al guardar la encuesta: {err}")
        return f"Error al guardar la encuesta: {err}", 500

    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"Error al guardar la encuesta: {err}", 500


# Ruta para buscar encuestas
@app.route("/buscar_encuestas")
def buscar_encuestas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()

    con.close()

    resultados = [{"Nombre_Apellido": r[1], "Comentario": r[2], "Calificacion": r[3]} for r in registros]

    return resultados

if __name__ == "__main__":
    app.run(debug=True)
