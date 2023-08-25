function editar_seccion(id) {
    // Redireccionar al formulario de edición con el ID del trabajador
    window.location.href = '/secciones2/' + id + '/edit';
}

function eliminar_seccion(id) {
    // Enviar una solicitud de eliminación del trabajador con el ID
    if (confirm("¿Estás seguro de que deseas eliminar este trabajador?")) {
        window.location.href = '/secciones2/' + id + '/delete';
    }
}