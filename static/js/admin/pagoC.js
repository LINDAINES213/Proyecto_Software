// Función para marcar una fila como pagada
function pagoRealizado2(button) {
  // Obtener la fila padre del botón
  var row2 = button.parentNode.parentNode;

  // Cambiar el color de fondo de la fila a verde claro
  row2.style.backgroundColor = "#B9E6C1";

  // Obtener el índice de la fila
  var rowIndex = row2.rowIndex;

  // Guardar la fecha de pago en el almacenamiento local como una marca de tiempo
  var fechaPago = Date.now();
  localStorage.setItem("fechaPago_" + rowIndex, fechaPago);

  // Iniciar un temporizador para revertir la fila después de 2 minutos
  setTimeout(function() {
    revertirFila(rowIndex);
  }, 12000); // 120000 ms = 2 minutos
}

function pagoPendiente2(button) {
  // Obtener la fila padre del botón
  var row2 = button.parentNode.parentNode;

  // Quitar el color de fondo de la fila
  row2.style.backgroundColor = "";

  // Obtener el índice de la fila
  var rowIndex = row2.rowIndex;

  // Eliminar la fecha de pago del almacenamiento local
  localStorage.removeItem("fechaPago_" + rowIndex);
}

window.onload = function() {
  // Iterar sobre todas las filas de la tabla
  var table = document.getElementsByTagName("table")[0];
  var rows2 = table.getElementsByTagName("tr");

  for (var i = 0; i < rows2.length; i++) {
    var row2 = rows2[i];

    // Obtener el índice de la fila
    var rowIndex = row2.rowIndex;

    // Verificar si la fecha de pago existe en el almacenamiento local
    var fechaPago = localStorage.getItem("fechaPago_" + rowIndex);

    if (fechaPago) {
      // Calcular el tiempo transcurrido en milisegundos
      var hoy = Date.now();
      var tiempoTranscurrido = hoy - parseInt(fechaPago, 10);

      // Si ha pasado más de 2 minutos, quitar el color verde
      if (tiempoTranscurrido > 12000) { // 120000 ms = 2 minutos
        revertirFila(rowIndex);
      } else {
        // Cambiar el color de fondo de la fila a verde claro
        row2.style.backgroundColor = "#B9E6C1";
      }
    }
  }
};

// Función para descargar la tabla en formato CSV
function descargarCSV() {
  const table = document.querySelector("table"); // Obtener la tabla
  const rows2 = table.querySelectorAll("tr");

  // Crear un array para almacenar los datos de la tabla
  const data = [];
  for (const row2 of rows2) {
      const rowData = [];
      
      // Obtener los títulos de las columnas (encabezados) excluyendo la última columna
      const headers = Array.from(row2.querySelectorAll("th")).slice(0, -1);
      for (const header of headers) {
          rowData.push(header.innerText);
      }

      // Obtener los datos de las celdas excluyendo la última columna
      const cells = Array.from(row2.querySelectorAll("td")).slice(0, -1);
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
  link.setAttribute("download", "pagosColegiaturas.csv");
  document.body.appendChild(link);

  // Simular el clic en el enlace para iniciar la descarga
  link.click();

  // Eliminar el enlace temporal
  document.body.removeChild(link);
}