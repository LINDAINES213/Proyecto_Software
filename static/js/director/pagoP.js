// Función para marcar una fila como pagada
function pagoRealizado(button) {
	var row = button.parentNode.parentNode;
	row.classList.add('pagado');
	guardarEstado(row);
}
	  
// Función para marcar una fila como pendiente
function pagoPendiente(button) {
	var row = button.parentNode.parentNode;
	row.classList.remove('pagado');
	guardarEstado(row);
}
	  
// Función para guardar el estado de la fila en el almacenamiento local
function guardarEstado(row) {
	var rowId = row.querySelector('td:first-child').textContent;
	var isPagado = row.classList.contains('pagado');
	localStorage.setItem('estadoFila-' + rowId, isPagado);
}
	  
// Función para cargar el estado de las filas desde el almacenamiento local
function cargarEstadoFilas() {
	var filas = document.querySelectorAll('tbody tr');
	filas.forEach(function(row) {
        var rowId = row.querySelector('td:first-child').textContent;
        var isPagado = localStorage.getItem('estadoFila-' + rowId);
        if (isPagado === 'true') {
            row.classList.add('pagado');
        }
	});
}
	  
// Cargar el estado de las filas cuando se carga la página
window.addEventListener('load', cargarEstadoFilas);  