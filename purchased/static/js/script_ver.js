function toggleSelectLists(item) {
    const selectLists = document.getElementById(`select-lists-${item}`);
    if (selectLists.style.display === "none") {
      selectLists.style.display = "block"; // Mostrar las listas
    } else {
      selectLists.style.display = "none"; // Ocultar las listas
    }
  }

  // Manejo del selector de empleado
  const empleadoSelect = document.getElementById('empleado');
  if (empleadoSelect) {
      empleadoSelect.addEventListener('change', function() {
          document.getElementById('empleado_hidden').value = this.value;
      });
  }

  // Función para ocultar todos los formularios
  function hideAllForms() {
    document.getElementById("proveedor-form").style.display = "none";
    document.getElementById("suministro-form").style.display = "none";
    document.getElementById("id_compra-form").style.display = "none";
  }

  // Botón para abrir form de agregar proveedor
  function toggleSupplierForm() {
    hideAllForms(); // Ocultamos todos los formularios
    var form = document.getElementById("proveedor-form");
    // Si el formulario está oculto, lo mostramos
    if (form.style.display === "none") {
      form.style.display = "block";
    }
  }

  // Botón para abrir form de agregar suministro
  function toggleInventoryForm() {
    hideAllForms(); // Ocultamos todos los formularios
    var form = document.getElementById("suministro-form");
    // Si el formulario está oculto, lo mostramos
    if (form.style.display === "none") {
      form.style.display = "block";
    }
  }

  // Botón para abrir form de agregar compras
  function toggleIdCompraForm() {
    hideAllForms(); // Ocultamos todos los formularios
    var form = document.getElementById("id_compra-form");
    // Si el formulario está oculto, lo mostramos
    if (form.style.display === "none") {
      form.style.display = "block";
    }
  }


  //agrega los items para agregar detalle_compras /// o salidass
  document.getElementById('add-detail-btn').addEventListener('click', function() {
    // Seleccionar el contenedor donde se agregan los detalles de compra
    var container = document.getElementById('detalle-compra-container');

    // Clonar la fila de detalle de compra
    var newDetailRow = document.querySelector('.detalle-compra-row').cloneNode(true);

    // Limpiar los valores de los campos clonados
    newDetailRow.querySelectorAll('input').forEach(function(input) {
      input.value = ''; // Limpiar el valor
    });
    newDetailRow.querySelector('select').selectedIndex = 0; // Reiniciar el select

    // Agregar la nueva fila al contenedor
    container.appendChild(newDetailRow);
  });

// Elimina los items para quitar detalle_compras /// o salidass
document.getElementById('del-detail-btn').addEventListener('click', function() {
  // Seleccionar el contenedor donde están los detalles de compra
  var container = document.getElementById('detalle-compra-container');

  // Seleccionar todas las filas de detalle de compra
  var detailRows = container.querySelectorAll('.detalle-compra-row');

  // Si hay más de una fila, eliminamos la última
  if (detailRows.length > 1) {
    container.removeChild(detailRows[detailRows.length - 1]);
  } else {
    alert("Debe haber al menos una fila de detalles de compra.");
  }
});