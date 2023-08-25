function editar_curso(id) {
    // Redireccionar al formulario de edición con el ID del trabajador
    window.location.href = '/cursos2/' + id + '/edit';
}

function eliminar_curso(id) {
    // Enviar una solicitud de eliminación del trabajador con el ID
    if (confirm("¿Estás seguro de que deseas eliminar este trabajador?")) {
        window.location.href = '/cursos2/' + id + '/delete';
    }
}