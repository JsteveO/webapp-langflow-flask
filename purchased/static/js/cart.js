// static/js/cart.js
window.CartManager = class CartManager {
    constructor() {
        this.carrito = [];
        this.sidebarRight = document.querySelector('.sidebar-right');
    }

    addToCart(producto, cantidad, precio, tipo, sabor) {
        const existingItem = this.carrito.find(item => 
            item.producto === producto && item.tipo === tipo && item.sabor === sabor
        );

        if (existingItem) {
            existingItem.cantidad = parseInt(existingItem.cantidad) + 1;

            // Actualizamos el input en el sidebar
            const cantidadInput = this.sidebarRight.querySelector(
                `.cantidad-input[data-producto="${producto}"][data-tipo="${tipo}"][data-sabor="${sabor}"]`
            );
            if (cantidadInput) {
                cantidadInput.value = existingItem.cantidad;
            }

        } else {
            this.carrito.push({ producto, cantidad, precio, tipo, sabor });
            this.addItemToSidebar({ producto, cantidad, precio, tipo, sabor });
        }

        this.updateCartDisplay();
    }

    addItemToSidebar(item) {
        const itemElement = document.createElement('div');
        itemElement.classList.add('cart-item');
        itemElement.innerHTML = `
            <div class="item-info">
                <strong>${item.producto}</strong><br>
                Detalle: ${item.tipo} - ${item.sabor}<br>
                Cantidad: <input type="number" value="${item.cantidad}" min="1" class="cantidad-input" data-producto="${item.producto}" data-tipo="${item.tipo}" data-sabor="${item.sabor}"><br>
                Precio: $${item.precio}
            </div>
            <div class="item-actions">
                <button class="remove-btn" data-producto="${item.producto}" data-tipo="${item.tipo}" data-sabor="${item.sabor}">X</button>
            </div>
        `;

        this.sidebarRight.insertBefore(itemElement, this.sidebarRight.querySelector('.total-label'));

        itemElement.querySelector('.remove-btn').addEventListener('click', () => {
            this.removeFromCart(item.producto, item.tipo, item.sabor);
            itemElement.remove();
        });

        itemElement.querySelector('.cantidad-input').addEventListener('input', (event) => {
            this.updateProductQuantity(item.producto, item.tipo, item.sabor, event.target.value);
        });
    }

    removeFromCart(producto, tipo, sabor) {
        this.carrito = this.carrito.filter(item => 
            !(item.producto === producto && item.tipo === tipo && item.sabor === sabor)
        );
        this.updateCartDisplay();
    }

    updateProductQuantity(producto, tipo, sabor, cantidad) {
        const product = this.carrito.find(item => 
            item.producto === producto && item.tipo === tipo && item.sabor === sabor
        );
        if (product) {
            product.cantidad = cantidad;
            this.updateCartDisplay();
        }
    }

    updateCartDisplay() {
        const totalLabel = document.querySelector('.sidebar-right .total-label span:last-child');
        let total = 0;

        this.carrito.forEach(item => {
            total += item.cantidad * item.precio;
        });

        totalLabel.textContent = `$${total.toFixed(2)}`;
    }

    updatePaymentForm(formPagar) {
        formPagar.querySelectorAll('input[name="producto"], input[name="cantidad"], input[name="precio"], input[name="tipo"], input[name="sabor"]').forEach(input => input.remove());

        this.carrito.forEach(item => {
            ['producto', 'cantidad', 'precio', 'tipo', 'sabor'].forEach(field => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = field;
                input.value = item[field];
                formPagar.appendChild(input);
            });
        });
    }
}