from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos (ajusta los parámetros según sea necesario)
db = mysql.connector.connect(
    host="185.232.14.52",
    user="tu_usuario",
    password="tu_contraseña",
    database="tu_base_de_datos"
)

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre_apellido = request.form['txtNombreApellido']
    comentario = request.form['txtComentario']
    calificacion = request.form['txtCalificacion']

    cursor = db.cursor()
    cursor.execute("INSERT INTO experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)",
                   (nombre_apellido, comentario, calificacion))
    db.commit()
    cursor.close()

    return jsonify({"message": "Experiencia registrada exitosamente."})

@app.route('/buscar', methods=['GET'])
def buscar():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM experiencias")
    resultados = cursor.fetchall()
    cursor.close()
    return jsonify(resultados)

@app.route('/experiencia/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM experiencias WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    return jsonify({"message": "Experiencia eliminada exitosamente."})

@app.route('/experiencia/actualizar/<int:id>', methods=['PUT'])
def actualizar(id):
    data = request.get_json()
    nuevo_nombre_apellido = data['nombre_apellido']
    nuevo_comentario = data['comentario']
    nueva_calificacion = data['calificacion']

    cursor = db.cursor()
    cursor.execute("""
        UPDATE experiencias
        SET Nombre_Apellido = %s, Comentario = %s, Calificacion = %s
        WHERE id = %s
    """, (nuevo_nombre_apellido, nuevo_comentario, nueva_calificacion, id))
    db.commit()
    cursor.close()

    return jsonify({"message": "Experiencia actualizada exitosamente."})

if __name__ == '__main__':
    app.run(debug=True)
