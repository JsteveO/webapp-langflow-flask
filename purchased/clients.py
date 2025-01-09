import os
import sys
from flask import Blueprint, render_template, request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pgadmin as pg
from products import productos

# Crear el blueprint para clientes
clientes_blueprint = Blueprint('clientes', __name__)

# Ruta para consultar y agregar clientes
@clientes_blueprint.route('/cliente', methods=['POST'])
def cliente():
    celphone = request.form.get('celular', '')
    agregar = 'crear' in request.form
    celu_prod = ''
    
    if agregar:
        # Obtener los datos del nuevo cliente
        new_cel = request.form.get('new_celular', '')
        new_name = request.form.get('cliente', '')
        new_address = request.form.get('direccion', '')
        
        # Crear un array con los datos del nuevo cliente
        nuevo_cliente = [new_cel, new_name, new_address]
        print(f"Nuevo cliente: {nuevo_cliente}")
        # Insertar el nuevo cliente en la base de datos
        resultado = pg.new_client(nuevo_cliente)
    else:
        # Consultar la base de datos para el celular ingresado
        df = pg.get_client(celphone)
        
        if not df.empty and celphone in df['phone'].values:
            points = df.loc[df['phone'] == celphone, 'points'].values[0]
            name = df.loc[df['phone'] == celphone, 'first_name'].values[0]
            resultado = f"{name} tiene {points} puntos. ID:"
            celu_prod = celphone

        else:
            resultado = "No existe."

    return render_template('home2.html', resultado=resultado, celular=celphone, productos=productos, celu_prod=celu_prod)
