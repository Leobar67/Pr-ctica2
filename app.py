from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

# Inicializar el cliente de Pusher
pusher_client = pusher.Pusher(
    app_id="1714541",
    key="2df86616075904231311",
    secret="2f91d936fd43d8e85a1a",
    cluster="us2",
    ssl=True
)

# Ruta principal
@app.route("/")
def index():
    return render_template("experiencias.html")

# Ruta para registrar una experiencia
@app.route("/registrar", methods=["POST"])
def registrar():
    nombre_apellido = request.form.get('txtNombreApellido')
    comentario = request.form.get('txtComentario')
    calificacion = request.form.get('txtCalificacion')

    if not nombre_apellido or not comentario or not calificacion:
        return jsonify({"status": "error", "message": "Faltan datos"})

    try:
        if not con.is_connected():
            con.reconnect()

        cursor = con.cursor()
        sql = "INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre_apellido, comentario, calificacion))
        con.commit()
        cursor.close()

        # Notificar a Pusher
        pusher_client.trigger("canalRegistrosexperiencias", "registroexperiencias", {
            'Nombre_Apellido': nombre_apellido,
            'Comentario': comentario,
            'Calificacion': calificacion
        })

        return jsonify({"status": "success", "message": "Experiencia registrada correctamente"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Ruta para buscar experiencias
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()
    cursor.close()

    # Convertir los registros en una lista de diccionarios
    experiencias = [
        {
            "Id_Experiencia": registro[0],
            "Nombre_Apellido": registro[1],
            "Comentario": registro[2],
            "Calificacion": registro[3]
        }
        for registro in registros
    ]
    return jsonify(experiencias)

# Ruta para eliminar una experiencia
@app.route("/experiencia/eliminar/<int:id>", methods=["DELETE"])
def eliminar_experiencia(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("DELETE FROM tst0_experiencias WHERE Id_Experiencia = %s", (id,))
    con.commit()
    cursor.close()

    # Notificar a Pusher
    pusher_client.trigger("canalRegistrosexperiencias", "registroexperiencias", {
        'message': 'Experiencia eliminada'
    })

    return jsonify({"status": "success", "message": "Experiencia eliminada correctamente"})

# Ruta para actualizar una experiencia
@app.route("/experiencia/actualizar/<int:id>", methods=["PUT"])
def actualizar_experiencia(id):
    data = request.get_json()  # Cambiado para recibir JSON
    nombre_apellido = data.get("nombre_apellido")
    comentario = data.get("comentario")
    calificacion = data.get("calificacion")

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute(""" 
        UPDATE tst0_experiencias 
        SET Nombre_Apellido = %s, Comentario = %s, Calificacion = %s 
        WHERE Id_Experiencia = %s 
    """, (nombre_apellido, comentario, calificacion, id))
    con.commit()
    cursor.close()

    # Notificar a Pusher sobre la actualización
    pusher_client.trigger("canalRegistrosexperiencias", "registroexperiencias", {
        'message': 'Experiencia actualizada'
    })

    return jsonify({"status": "success", "message": "Experiencia actualizada correctamente"})

# Ruta para obtener una experiencia específica por ID
@app.route("/experiencia/<int:id>")
def obtener_experiencia(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias WHERE Id_Experiencia = %s", (id,))
    experiencia = cursor.fetchone()
    cursor.close()

    if experiencia:
        return jsonify({
            "Id_Experiencia": experiencia[0],
            "Nombre_Apellido": experiencia[1],
            "Comentario": experiencia[2],
            "Calificacion": experiencia[3]
        })
    else:
        return jsonify({"status": "error", "message": "Experiencia no encontrada"}), 404

if __name__ == "__main__":
    app.run(debug=True)
