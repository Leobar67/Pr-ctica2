<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Encuesta de Experiencia</title>
    <!-- Incluir Bootstrap y jQuery -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.3/jquery.validate.min.js"></script>
</head>
<body>
    <div class="container">
        <h2>Encuesta de Experiencia</h2>
        
        <form id="encuestaForm">
            <div class="form-group">
                <label for="Id_Experiencia">ID de Experiencia:</label>
                <input type="number" class="form-control" id="Id_Experiencia" name="Id_Experiencia" required>
            </div>
            <div class="form-group">
                <label for="Nombre_Apellido">Nombre y Apellido:</label>
                <input type="text" class="form-control" id="Nombre_Apellido" name="Nombre_Apellido" required minlength="10" maxlength="50">
            </div>
            <div class="form-group">
                <label for="Comentario">Comentario:</label>
                <textarea class="form-control" id="Comentario" name="Comentario" required minlength="10" maxlength="50"></textarea>
            </div>
            <div class="form-group">
                <label for="Calificacion">Calificación:</label>
                <input type="number" class="form-control" id="Calificacion" name="Calificacion" required min="0" max="5">
            </div>
            <button type="submit" class="btn btn-primary">Calificar</button>
        </form>
    </div>

    <script>
        // Validación del formulario con jQuery
        $(document).ready(function() {
            $("#encuestaForm").validate({
                messages: {
                    Id_Experiencia: {
                        required: "Por favor, introduce un ID de experiencia."
                    },
                    Nombre_Apellido: {
                        required: "Por favor, introduce tu nombre y apellido.",
                        minlength: "Debes introducir al menos 10 caracteres.",
                        maxlength: "No puedes exceder los 50 caracteres."
                    },
                    Comentario: {
                        required: "Por favor, introduce un comentario.",
                        minlength: "Debes introducir al menos 10 caracteres.",
                        maxlength: "No puedes exceder los 50 caracteres."
                    },
                    Calificacion: {
                        required: "Por favor, introduce una calificación.",
                        min: "La calificación mínima es 0.",
                        max: "La calificación máxima es 5."
                    }
                }
            });
        });
    </script>
</body>
</html>
