// Función para marcar una fila como pagada
function pagoRealizado(button) {
  // Obtener la fila padre del botón
  var row = button.parentNode.parentNode;

  // Cambiar el color de fondo de la fila a verde claro
  row.style.backgroundColor = "#B9E6C1";

  // Obtener el índice de la fila
  var rowIndex = row.rowIndex;

  // Guardar la fecha de pago en el almacenamiento local como una marca de tiempo
  var fechaPago = Date.now();
  localStorage.setItem("fechaPago_" + rowIndex, fechaPago);

  // Iniciar un temporizador para revertir la fila después de 35 días
  setTimeout(function() {
    revertirFila(rowIndex);
  }, 35 * 24 * 60 * 60 * 1000); // 35 días en milisegundos
}

function pagoPendiente(button) {
  // Obtener la fila padre del botón
  var row = button.parentNode.parentNode;

  // Quitar el color de fondo de la fila
  row.style.backgroundColor = "";

  // Obtener el índice de la fila
  var rowIndex = row.rowIndex;

  // Eliminar la fecha de pago del almacenamiento local
  localStorage.removeItem("fechaPago_" + rowIndex);
}

window.onload = function() {
  // Iterar sobre todas las filas de la tabla
  var table = document.getElementsByTagName("table")[0];
  var rows = table.getElementsByTagName("tr");

  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];

    // Obtener el índice de la fila
    var rowIndex = row.rowIndex;

    // Verificar si la fecha de pago existe en el almacenamiento local
    var fechaPago = localStorage.getItem("fechaPago_" + rowIndex);

    if (fechaPago) {
      // Calcular el tiempo transcurrido en milisegundos
      var hoy = Date.now();
      var tiempoTranscurrido = hoy - parseInt(fechaPago, 10);

      // Si ha pasado más de 35 días, quitar el color verde
      if (tiempoTranscurrido > 35 * 24 * 60 * 60 * 1000) { // 35 días en milisegundos
        revertirFila(rowIndex);
      } else {
        // Cambiar el color de fondo de la fila a verde claro
        row.style.backgroundColor = "#B9E6C1";
      }
    }
  }
};

function descargarTablaComoPDF() {
  // Crear un nuevo objeto jsPDF
  var doc = new jsPDF();

  // Agregar contenido a la página
  doc.text("Tabla de Pagos", 10, 10);

  // Capturar la tabla
  var table = document.getElementsByTagName("table")[0];
  var res = doc.autoTableHtmlToJson(table);

  // Agregar la tabla al documento
  doc.autoTable({
    head: [res.columns],
    body: res.data,
    startY: 20
  });

  // Guardar el PDF como un archivo descargable
  doc.save("tabla_de_pagos.pdf");
};

/*// Función para marcar una fila como pagada
function pagoRealizado(button) {
  // Obtener la fila padre del botón
  var row = button.parentNode.parentNode;

  // Cambiar el color de fondo de la fila a verde claro
  row.style.backgroundColor = "#B9E6C1";

  // Obtener el índice de la fila
  var rowIndex = row.rowIndex;

  // Guardar la fecha de pago en el almacenamiento local como una marca de tiempo
  var fechaPago = Date.now();
  localStorage.setItem("fechaPago_" + rowIndex, fechaPago);

  // Iniciar un temporizador para revertir la fila después de 2 minutos
  setTimeout(function() {
    revertirFila(rowIndex);
  }, 120000); // 120000 ms = 2 minutos
}

function pagoPendiente(button) {
  // Obtener la fila padre del botón
  var row = button.parentNode.parentNode;

  // Quitar el color de fondo de la fila
  row.style.backgroundColor = "";

  // Obtener el índice de la fila
  var rowIndex = row.rowIndex;

  // Eliminar la fecha de pago del almacenamiento local
  localStorage.removeItem("fechaPago_" + rowIndex);
}

window.onload = function() {
  // Iterar sobre todas las filas de la tabla
  var table = document.getElementsByTagName("table")[0];
  var rows = table.getElementsByTagName("tr");

  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];

    // Obtener el índice de la fila
    var rowIndex = row.rowIndex;

    // Verificar si la fecha de pago existe en el almacenamiento local
    var fechaPago = localStorage.getItem("fechaPago_" + rowIndex);

    if (fechaPago) {
      // Calcular el tiempo transcurrido en milisegundos
      var hoy = Date.now();
      var tiempoTranscurrido = hoy - parseInt(fechaPago, 10);

      // Si ha pasado más de 2 minutos, quitar el color verde
      if (tiempoTranscurrido > 120000) { // 120000 ms = 2 minutos
        revertirFila(rowIndex);
      } else {
        // Cambiar el color de fondo de la fila a verde claro
        row.style.backgroundColor = "#B9E6C1";
      }
    }
  }
};*/