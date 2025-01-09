window.handleSelectorChange = function(itemName, selectorType) {
    const selector = document.getElementById(`list${selectorType}-${itemName}`);
    const input = document.getElementById(`${selectorType === 1 ? 'tipo' : 'sabor'}-${itemName}`);
    const saborSelect = document.getElementById(`list2-${itemName}`);

    if (!selector) {
        window.updatePrice(itemName);
        return;
    }

    if (selector && input) {
        selector.addEventListener('change', function() {
            input.value = this.value;

            if (selectorType === 1 && this.value === "cremoso") {
                saborSelect.style.display = "block";
                saborSelect.innerHTML = `
                    <option value="" disabled selected>Sabor</option>
                    <option value="Baileys">Baileys</option>
                    <option value="Cocoloko">Cocoloko</option>
                    <option value="Mixto">Mixto</option>
                `;
            } 
            else if (selectorType === 1 && this.value === "alcohol") {
                saborSelect.style.display = "block";
                saborSelect.innerHTML = `
                    <option value="" disabled selected>Sabor</option>
                    <option value="Rose">Rose</option>
                    <option value="Ojo_diablo">Ojo de diablo</option>
                    <option value="Jagermeister">Jagermeister</option>
                    <option value="Manzana Verde">Manzana Verde</option>
                    <option value="Mixto">Mixto</option>
                `;
            }
            else if (selectorType === 1 && this.value === "juice") {
                saborSelect.style.display = "block";
                saborSelect.innerHTML = `
                    <option value="" disabled selected>Sabor</option>
                    <option value="Fresa">None</option>

                `;
            }

            window.updatePrice(itemName);
        });
    }
};

window.updatePrice = function(itemName) {
    const list1 = document.getElementById(`list1-${itemName}`);
    let totalPrecio = 0;

    if (list1 && list1.value) {
        const tipo = list1.value;
        if (window.precios[itemName] && window.precios[itemName][tipo]) {
            totalPrecio = window.precios[itemName][tipo];
        } else {
            console.error(`No se encontró un precio para el tipo "${tipo}" de "${itemName}"`);
        }
    } else {
        if (window.precios[itemName]) {
            const productoPrecio = Object.values(window.precios[itemName])[0];
            totalPrecio = productoPrecio;
        } else {
            console.error(`No se encontró un precio para "${itemName}"`);
        }
    }

    const precioVista = document.getElementById(`precio-vista-${itemName}`);
    if (precioVista) {
        precioVista.textContent = `Precio: $${totalPrecio}`;
    }

    const precioInput = document.querySelector(`input[name="precio"][id="precio-${itemName}"]`);
    if (precioInput) {
        precioInput.value = totalPrecio;
    }
};