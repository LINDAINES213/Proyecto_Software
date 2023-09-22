// Función para marcar una fila como pagada
function pagoRealizado(button) {
  // Obtener la fila padre del botón
  var row = button.parentNode.parentNode;
  
  // Cambiar el color de fondo de la fila a verde claro
  row.style.backgroundColor = "#B9E6C1";
  
  // Obtener el índice de la fila
  var rowIndex = row.rowIndex;
  
  // Guardar el índice de la fila en el almacenamiento local
  localStorage.setItem("filaPintada_" + rowIndex, "pagado");
}

function pagoPendiente(button) {
    // Obtener la fila padre del botón
    var row = button.parentNode.parentNode;
  
    // Quitar el color de fondo de la fila
    row.style.backgroundColor = "";
  
    // Obtener el índice de la fila
    var rowIndex = row.rowIndex;
  
    // Eliminar el estado de la fila del almacenamiento local
    localStorage.removeItem("filaPintada_" + rowIndex);
  }

window.onload = function() {
    // Iterar sobre todas las filas de la tabla
    var table = document.getElementsByTagName("table")[0];
    var rows = table.getElementsByTagName("tr");
    
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      
      // Obtener el índice de la fila
      var rowIndex = row.rowIndex;
      
      // Verificar si la fila está pintada en el almacenamiento local
      if (localStorage.getItem("filaPintada_" + rowIndex) === "pagado") {
        // Cambiar el color de fondo de la fila a verde claro
        row.style.backgroundColor = "#B9E6C1";
      }
    }
};

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
  link.setAttribute("download", "pagosSalarios.csv");
  document.body.appendChild(link);

  // Simular el clic en el enlace para iniciar la descarga
  link.click();

  // Eliminar el enlace temporal
  document.body.removeChild(link);
}