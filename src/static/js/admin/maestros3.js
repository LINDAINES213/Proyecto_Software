function editar_maestro(dpi) {
    // Redireccionar al formulario de edición con el ID del trabajador
    window.location.href = '/maestros2/' + dpi + '/edit';
}

function eliminar_maestro(dpi) {
    // Enviar una solicitud de eliminación del trabajador con el ID
    if (confirm("¿Estás seguro de que deseas eliminar este trabajador?")) {
        window.location.href = '/maestros2/' + dpi + '/delete';
    }
}