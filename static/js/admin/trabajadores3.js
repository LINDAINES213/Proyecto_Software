function editWorker(dpi) {
    // Redireccionar al formulario de edición con el ID del trabajador
    window.location.href = '/trabajadores2/' + dpi + '/edit';
}

function deleteWorker(dpi) {
    // Enviar una solicitud de eliminación del trabajador con el ID
    if (confirm("¿Estás seguro de que deseas eliminar este trabajador?")) {
        window.location.href = '/trabajadores2/' + dpi + '/delete';
    }
}