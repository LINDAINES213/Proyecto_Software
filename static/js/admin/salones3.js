function editar_salon(id) {
    // Redireccionar al formulario de edición con el ID del trabajador
    window.location.href = '/salones2/' + id + '/edit';
}

function eliminar_salon(id) {
    // Enviar una solicitud de eliminación del trabajador con el ID
    if (confirm("¿Estás seguro de que deseas eliminar este salón?")) {
        window.location.href = '/salones2/' + id + '/delete';
    }
}