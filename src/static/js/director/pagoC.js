// Función para marcar como pagado
function pagoRealizado(button) {
    var row = button.parentNode.parentNode;
	row.classList.add('pagado');
	var id = row.id.replace('fila-', '');
	localStorage.setItem(id, 'pagado');
}

// Función para marcar como pendiente
function pagoPendiente(button) {
	var row = button.parentNode.parentNode;
	row.classList.remove('pagado');
	var id = row.id.replace('fila-', '');
	localStorage.setItem(id, 'pendiente');
}

// Al cargar la página, verificar el estado de cada fila
window.onload = function() {
	var rows = document.getElementsByTagName('tr');
	for (var i = 0; i < rows.length; i++) {
		var id = rows[i].id.replace('fila-', '');
		var estado = localStorage.getItem(id);
		if (estado === 'pagado') {
			rows[i].classList.add('pagado');
		} else {
			rows[i].classList.remove('pagado');
		}
	}
};
