 // Función para obtener el valor de una cookie por su nombre
 function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Buscar la cookie por su nombre y obtener su valor
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    
function mostrarMensaje(message) {
if (message === 'success') {
  // Mostrar el mensaje de éxito del servidor
  Swal.fire({
      title: 'Éxito',
      text: 'El archivo se ha cargado correctamente.',
      icon: 'success',
  });
} else if (message === 'error') {
  // Mostrar el mensaje de error del servidor
  Swal.fire({
      title: 'Error',
      text: 'Ha ocurrido un error durante la carga del archivo.',
      icon: 'error',
  });
}
}
    // Obtener el token CSRF de la cookie
    var csrftoken = getCookie('csrftoken');
    // Manejo de mensajes flash de Django
    $('#cargar-form').submit(function(e) {
        e.preventDefault();
        // Deshabilitar el botón y mostrar el spinner de carga
        $('#cargar-button').prop('disabled', true);
        $('#cargar-spinner').show();
        // Serializar el formulario completo
        var formData = new FormData($(this)[0]);
        // Realizar la solicitud AJAX al servidor
        $.ajax({
            type: 'POST',
            url: "{% url 'cargar' %}",
            data: formData,
            contentType: false,
            processData: false,
            headers: { "X-CSRFToken": csrftoken }, // Agregar el token CSRF a los encabezados
            success: function(data) {
                // Habilitar el botón y ocultar el spinner
                $('#cargar-button').prop('disabled', false);
                $('#cargar-spinner').hide();
                // Mostrar el mensaje de éxito del servidor
                mostrarMensaje(data.message);
            },
            error: function() {
                // Mostrar el mensaje de error del servidor
                mostrarMensaje('error');
            }
        });
    });
});