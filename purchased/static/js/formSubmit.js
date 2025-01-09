// static/js/scripts.js
window.addEventListener('DOMContentLoaded', function () {
    window.cartManager = new window.CartManager();
    const forms = document.querySelectorAll('.add-to-cart-form');
    const formPagar = document.querySelector('form[action="/pagar"]');

    // Inicializar selectores
    const productos = document.querySelectorAll('.card');
    productos.forEach(producto => {
        const itemName = producto.querySelector('.card-title').textContent;
        window.handleSelectorChange(itemName, 1);
        
        const list2 = document.getElementById(`list2-${itemName}`);
        if (list2) {
            window.handleSelectorChange(itemName, 2);
        }
    });

    // Manejar formularios de agregar al carrito
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
                    window.cartManager.addToCart(producto, cantidad, precio, tipo, sabor);
                } else {
                    alert("Por favor, completa todos los campos antes de agregar al carrito.");
                }
            }
            else if (category === "Micheladas") {
                if (producto && cantidad && precio && tipo) {
                    window.cartManager.addToCart(producto, cantidad, precio, tipo, sabor);
                } else {
                    alert("Por favor, completa todos los campos antes de agregar al carrito.");
                }
            }
            else {
                window.cartManager.addToCart(producto, cantidad, precio, tipo, sabor);
            }
        });
    });

    // Manejar formulario de pago
    if (formPagar) {
        formPagar.addEventListener('submit', function (event) {
            window.cartManager.updatePaymentForm(this);
        });
    }
});