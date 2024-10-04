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
    return render_template("experiencias.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()

    con.close()
    return jsonify(registros)

@app.route("/registrar", methods=["POST"])
def registrar():
    nombre_apellido = request.form.get('txtNombreApellido')
    comentario = request.form.get('txtComentario')
    calificacion = request.form.get('txtCalificacion')

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre_apellido, comentario, calificacion))
    con.commit()
    cursor.close()
    con.close()

    pusher_client.trigger("canalRegistrosexperiencias", "registroexperiencias", {
        'Nombre_Apellido': nombre_apellido,
        'Comentario': comentario,
        'Calificacion': calificacion
    })

    return {"status": "success", "message": "Datos guardados correctamente"}

@app.route("/experiencia/<int:id>")
def obtener_experiencia(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_experiencias WHERE Id_Experiencia = %s", (id,))
    experiencia = cursor.fetchone()

    con.close()
    return jsonify(experiencia)

@app.route("/actualizar", methods=["POST"])
def actualizar_experiencia():
    id_experiencia = request.form.get('id_experiencia')
    nombre_apellido = request.form.get('txtNombreApellido')
    comentario = request.form.get('txtComentario')
    calificacion = request.form.get('txtCalificacion')

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = """
        UPDATE tst0_experiencias 
        SET Nombre_Apellido = %s, Comentario = %s, Calificacion = %s 
        WHERE Id_Experiencia = %s
    """
    cursor.execute(sql, (nombre_apellido, comentario, calificacion, id_experiencia))
    con.commit()
    cursor.close()
    con.close()

    pusher_client.trigger("canalRegistrosexperiencias", "registroexperiencias", {
        'Nombre_Apellido': nombre_apellido,
        'Comentario': comentario,
        'Calificacion': calificacion,
        'Id_Experiencia': id_experiencia
    })

    return {"status": "success", "message": "Experiencia actualizada correctamente"}

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_experiencia(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "DELETE FROM tst0_experiencias WHERE Id_Experiencia = %s"
    cursor.execute(sql, (id,))
    con.commit()
    cursor.close()
    con.close()

    pusher_client.trigger("canalRegistrosexperiencias", "eliminarexperiencia", {
        'Id_Experiencia': id
    })

    return {"status": "success", "message": "Experiencia eliminada correctamente"}

if __name__ == "__main__":
    app.run(debug=True)
