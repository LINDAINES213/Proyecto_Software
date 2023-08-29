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