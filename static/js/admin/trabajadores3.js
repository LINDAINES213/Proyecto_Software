function editWorker(dpi) {
    // Redireccionar al formulario de edición con el ID del trabajador
    window.location.href = '/trabajadores2/' + dpi + '/edit';
}

function deleteWorker(dpi) {
    // Enviar una solicitud de eliminación del trabajador con el ID
    
    window.location.href = '/trabajadores2/' + dpi + '/delete';

}

// Función para descargar la tabla en formato CSV
function descargarCSV() {
    const table = document.querySelector("table"); // Obtener la tabla
    const rows = table.querySelectorAll("tr");

    // Crear un array para almacenar los datos de la tabla
    const data = [];
    for (const row of rows) {
        const rowData = [];
        
        // Obtener los títulos de las columnas (encabezados) excluyendo la última columna
        const headers = Array.from(row.querySelectorAll("th")).slice(0, -1);
        for (const header of headers) {
            rowData.push(header.innerText);
        }

        // Obtener los datos de las celdas excluyendo la última columna
        const cells = Array.from(row.querySelectorAll("td")).slice(0, -1);
        for (const cell of cells) {
            rowData.push(cell.innerText);
        }

        data.push(rowData.join(","));
    }

    // Crear un enlace temporal para descargar el archivo CSV
    const csvContent = "data:text/csv;charset=utf-8," + data.join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "trabajadores.csv");
    document.body.appendChild(link);

    // Simular el clic en el enlace para iniciar la descarga
    link.click();

    // Eliminar el enlace temporal
    document.body.removeChild(link);
}

window.onbeforeunload = function(event) {
    // Verificar si la ruta actual es la que deseas redirigir
    if (window.location.pathname === "/trabajadores3") {
      // Redirigir a la ruta deseada
      window.location.href = "/inicioadmin";
    }
  };