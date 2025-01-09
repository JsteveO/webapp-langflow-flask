// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.add-to-cart-form');
    const formPagar = document.querySelector('form[action="/pagar"]');
    let carrito = [];
    const precios = {
        "Granizado XL": {
            "alcohol": 55000,
            "juice": 55000,
            "cremoso": 65000
        },
        "Granizado XXL": {
            "juice": 80000,
            "cremoso": 100000,
            "alcohol": 80000
        },
        "Michelada Mango": {
            "aguila": 10000,
            "corona": 13000,
            "quatro": 8000
        },
        "Michelada Cereza": {
            "aguila": 11000,
            "corona": 14000,
            "quatro": 9000
        },
        "Michelada Maracuyá": {
            "aguila": 10000,
            "corona": 13000,
            "quatro": 8000
        },
        "Granizado Grande": {
            "alcohol": 20000,
            "juice": 20000,
            "cremoso": 23000
        },
        "Granizado Pequeño": {
            "alcohol": 8000,
            "juice": 8000,
            "cremoso": 10000
        },
        "Granizado Mediano": {
            "alcohol": 12000,
            "juice": 12000,
            "cremoso": 15000
        },
        "Águila light": {
            "cerveza": 5000
        },
        "Corona": {
            "cerveza": 10000
        },
        "Fourloko": {
            "Bebida Alcholica": 20000
        },
        "Like": {
            "Bebida Alcholica": 12000
        },
        "Gatorade": {
            "Bebida Hidratante": 4000
        }
        // Agrega más productos según sea necesario
    };

// Función para manejar los cambios en los selectores
function handleSelectorChange(itemName, selectorType) {
    const selector = document.getElementById(`list${selectorType}-${itemName}`);
    const input = document.getElementById(`${selectorType === 1 ? 'tipo' : 'sabor'}-${itemName}`);
    const saborSelect = document.getElementById(`list2-${itemName}`);  // Select de sabor

    // Si no hay selector (producto sin tipo o sabor), actualizar directamente el precio
    if (!selector) {
        updatePrice(itemName);
        return; // Salir de la función si no hay selectores
    }

    // Si hay selector, agregar un listener para cambios en el selector
    if (selector && input) {
        selector.addEventListener('change', function() {
            input.value = this.value;

            // Mostrar el select de sabores basados en el tipo seleccionado
            if (selectorType === 1 && this.value === "cremoso") {
                saborSelect.style.display = "block";  // Mostrar el select de sabor
                saborSelect.innerHTML = `
                    <option value="" disabled selected>Sabor</option>
                    <option value="Baileys">Baileys</option>
                    <option value="Maracumango">Maracumango</option>
                `;
            } 
            else if (selectorType === 1 && this.value === "alcohol") {
                saborSelect.style.display = "block";  // Mostrar el select de sabor
                saborSelect.innerHTML = `
                    <option value="" disabled selected>Sabor</option>
                    <option value="Fresa">Fresa</option>
                    <option value="Morazul">Morazul</option>
                    <option value="Ojo_diablo">Ojo de diablo</option>
                `;
            }
            else if (selectorType === 1 && this.value === "juice") {
                saborSelect.style.display = "block";  // Mostrar el select de sabor
                saborSelect.innerHTML = `
                    <option value="" disabled selected>Sabor</option>
                    <option value="Fresa">Fresa</option>
                    <option value="Morazul">Morazul</option>
                    <option value="Ojo_diablo">Ojo de diablo</option>
                `;
            }

            // Actualizar el precio en función del tipo y sabor seleccionados
            updatePrice(itemName);
        });
    }
}

// Función para actualizar el precio
function updatePrice(itemName) {
    const list1 = document.getElementById(`list1-${itemName}`);
    let totalPrecio = 0;

    if (list1 && list1.value) {
        // Es un producto con opciones (Granizados o Micheladas)
        const tipo = list1.value;

        // Verificar si el tipo seleccionado está en el diccionario de precios
        if (precios[itemName] && precios[itemName][tipo]) {
            totalPrecio = precios[itemName][tipo];
        } else {
            console.error(`No se encontró un precio para el tipo "${tipo}" de "${itemName}"`);
        }
    } else {
        // Producto sin selectores de tipo (ni list1 ni list2)
        if (precios[itemName]) {
            // Usar el primer precio del objeto como valor predeterminado
            const productoPrecio = Object.values(precios[itemName])[0];
            totalPrecio = productoPrecio;
        } else {
            console.error(`No se encontró un precio para "${itemName}"`);
        }
    }

    // Actualizar el div de visualización del precio
    const precioVista = document.getElementById(`precio-vista-${itemName}`);
    if (precioVista) {
        precioVista.textContent = `Precio: $${totalPrecio}`;
    }

    // Actualizar el input oculto de precio
    const precioInput = document.querySelector(`input[name="precio"][id="precio-${itemName}"]`);
    if (precioInput) {
        precioInput.value = totalPrecio; // Actualizar el valor del input oculto
    }
}



// Asumimos que hay una función que inicializa los selectores cuando la página carga
// Si no hay selectores de tipo y sabor para algunos productos, el precio se actualizará automáticamente
function initializeSelectors(items) {
    items.forEach(itemName => {
        handleSelectorChange(itemName, 1); // Inicializar el selector de tipo (1)
        handleSelectorChange(itemName, 2); // Inicializar el selector de sabor (2)
    });
}

    // Configurar los event listeners para los selectores de cada producto
    const productos = document.querySelectorAll('.card');
    productos.forEach(producto => {
        const itemName = producto.querySelector('.card-title').textContent;
        
        // Configurar para el primer selector (tipo)
        handleSelectorChange(itemName, 1);
        
        // Configurar para el segundo selector (sabor), si existe
        const list2 = document.getElementById(`list2-${itemName}`);
        if (list2) {
            handleSelectorChange(itemName, 2);
        }
    });

    // Manejo de formularios de agregar al carrito
    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const category = this.querySelector('input[name="category"]').value;
            const producto = this.querySelector('input[name="producto"]').value;
            const cantidad = this.querySelector('input[name="cantidad"]').value;
            const precio = this.querySelector('input[name="precio"]').value;
            const tipo = this.querySelector('input[name="tipo"]').value;
            const sabor = this.querySelector('input[name="sabor"]').value;
            
            if (category === "Granizados") {
                if (producto && cantidad && precio && tipo && sabor) {
                    addToCart(producto, cantidad, precio, tipo, sabor);  // Agregar al carrito sin recargar la página
                } else {
                    alert("Por favor, completa todos los campos antes de agregar al carrito.");
                }
                }
            else if (category === "Micheladas") {
                if (producto && cantidad && precio && tipo) {
                    addToCart(producto, cantidad, precio, tipo, sabor);  // Agregar al carrito sin recargar la página
                } else {
                    alert("Por favor, completa todos los campos antes de agregar al carrito.");
                }
                }
            else {addToCart(producto, cantidad, precio, tipo, sabor);}
        });
    });

        // Función para agregar productos al carrito y al sidebar
    function addToCart(producto, cantidad, precio, tipo, sabor) {
        const sidebarRight = document.querySelector('.sidebar-right');

        // Comparar también el tipo y el sabor
        const existingItem = carrito.find(item => 
            item.producto === producto && item.tipo === tipo && item.sabor === sabor
        );

        if (existingItem) {
            existingItem.cantidad = parseInt(existingItem.cantidad) + parseInt(cantidad);
            updateCartDisplay();
        } else {
            carrito.push({ producto, cantidad, precio, tipo, sabor });

            const item = document.createElement('div');
            item.classList.add('cart-item');
            item.innerHTML = `
                <div class="item-info">
                    <strong>${producto}</strong><br>
                    Detalle: ${tipo} - ${sabor}<br>
                    Cantidad: <input type="number" value="${cantidad}" min="1" class="cantidad-input" data-producto="${producto}" data-tipo="${tipo}" data-sabor="${sabor}"><br>
                    Precio: $${precio}
                </div>
                <div class="item-actions">
                    <button class="remove-btn" data-producto="${producto}" data-tipo="${tipo}" data-sabor="${sabor}">X</button>
                </div>
            `;

            sidebarRight.insertBefore(item, sidebarRight.querySelector('.total-label'));

            item.querySelector('.remove-btn').addEventListener('click', function () {
                removeFromCart(producto, tipo, sabor);
                item.remove();
            });

            item.querySelector('.cantidad-input').addEventListener('input', function () {
                updateProductQuantity(producto, tipo, sabor, this.value);
            });
        }

        updateCartDisplay();
    }

    // Función para actualizar la cantidad de un producto específico por tipo y sabor
    function updateProductQuantity(producto, tipo, sabor, cantidad) {
        const product = carrito.find(item => 
            item.producto === producto && item.tipo === tipo && item.sabor === sabor
        );
        if (product) {
            product.cantidad = cantidad;
            updateCartDisplay();
        }
    }

// Función para eliminar un producto específico del carrito
    function removeFromCart(producto, tipo, sabor) {
        carrito = carrito.filter(item => 
            !(item.producto === producto && item.tipo === tipo && item.sabor === sabor)
        );
        updateCartDisplay();
}

    // Función para actualizar el total del carrito en la interfaz
    function updateCartDisplay() {
        const totalLabel = document.querySelector('.sidebar-right .total-label span:last-child');
        let total = 0;

        carrito.forEach(item => {
            total += item.cantidad * item.precio;
        });

        totalLabel.textContent = `$${total.toFixed(2)}`;
    }

    // Actualizar el formulario de pago antes de enviarlo
    formPagar.addEventListener('submit', function (event) {
        formPagar.querySelectorAll('input[name="producto"], input[name="cantidad"], input[name="precio"], input[name="tipo"], input[name="sabor"]').forEach(input => input.remove());

        carrito.forEach(item => {
            ['producto', 'cantidad', 'precio', 'tipo', 'sabor'].forEach(field => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = field;
                input.value = item[field];
                formPagar.appendChild(input);
            });
        });
    });

});