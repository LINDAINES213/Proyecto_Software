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