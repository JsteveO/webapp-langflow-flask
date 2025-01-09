import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pgadmin as pg

# Crear el blueprint para productos
productos_blueprint = Blueprint('productos', __name__)

# Definir la lista de productos
products = pg.get_products()

precios = {
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
        "Smirnoff": {
            "Bebida Alcholica": 12000
        },
        "Gatorade": {
            "Bebida Hidratante": 4000
        }
    }

productos = {
    'Granizados': [
        {'nombre': 'Granizado Pequeño', 'imagen': '8oz.png'},
        {'nombre': 'Granizado Mediano', 'imagen': '16oz.png'},
        {'nombre': 'Granizado Grande', 'imagen': '16oz.png'},
        {'nombre': 'Granizado XL', 'imagen': '3L.png'},
        {'nombre': 'Granizado XXL', 'imagen': '5L.png'}
    ],
    'Micheladas': [
        {'nombre': 'Michelada Cereza', 'imagen': 'ov.png'},
        {'nombre': 'Michelada Mango', 'imagen': 'ov.png'},
        {'nombre': 'Michelada Maracuyá', 'imagen': 'ov.png'}
    ],
    'Bebida Alcoholica': [
        {'nombre': 'Mini Vodka', 'imagen': 'ov.png'},
        {'nombre': 'Mini Jagermeister', 'imagen': 'ov.png'},
        {'nombre': 'Aguardiente Azul Tetra', 'imagen': 'ov.png'},
        {'nombre': 'Aguardiente Verde Tetra', 'imagen': 'ov.png'},
        {'nombre': 'Ron Caldas Tetra', 'imagen': 'ov.png'},
        {'nombre': 'Vodka Smirnoff', 'imagen': 'ov.png'},
        {'nombre': 'Media Ron Caldas', 'imagen': 'ov.png'},
        {'nombre': 'Media Aguardiente Azul', 'imagen': 'ov.png'},
        {'nombre': 'Media Aguardiente Verde', 'imagen': 'ov.png'},
        {'nombre': 'Fourloko', 'imagen': 'ov.png'},
        {'nombre': 'Smirnoff', 'imagen': 'ov.png'},
    ],
    'Hidratante': [
        {'nombre': 'Gatorade', 'imagen': 'ov.png'},
        {'nombre': 'Redbull', 'imagen': 'ov.png'},
        {'nombre': 'Electrolit', 'imagen': 'ov.png'},
        {'nombre': 'Coca cola', 'imagen': 'ov.png'},
        {'nombre': 'Soda', 'imagen': 'ov.png'},
        {'nombre': 'Agua botella', 'imagen': 'ov.png'},
    ],
    'Cerveza': [
        {'nombre': 'Águila light', 'imagen': 'ov.png'},
        {'nombre': 'Águila original', 'imagen': 'ov.png'},
        {'nombre': 'Laton Águila light', 'imagen': 'ov.png'},
        {'nombre': 'Botella Águila L', 'imagen': 'ov.png'},
        {'nombre': 'Pilsen', 'imagen': 'ov.png'},
        {'nombre': 'Corona', 'imagen': 'ov.png'},
        {'nombre': 'Coronita', 'imagen': 'ov.png'},
        {'nombre': 'Club Colombia', 'imagen': 'ov.png'}
    ]
}

pago = {'transferencia': 1,
           'efectivo': 2,
           'particion': 4}

empleados = {'saimon': 1,
           'stiven': 2}

sabores = {
    "Granizados": {
        "Rose": 20,
        "Jagermeister": 19,
        "Ojo_diablo": 3,
        "Cocoloko": 21,
        "Baileys": 5,
        "Incognito": 22,
        "Mixto": 22}
        }

# Ruta para mostrar los productos
@productos_blueprint.route('/pagar', methods=['POST'])
def pagar():
    # Obtener los datos del carrito desde la solicitud

    carrito = {'producto': request.form.getlist('producto'),
               'tipo': request.form.getlist('tipo'),
               'sabor': request.form.getlist('sabor'),
               'cantidades': request.form.getlist('cantidad'),
               'precios': request.form.getlist('precio'),
               'tipo_pago': request.form.get('tipo_pago', ''),
               'descuento': request.form.get('descuento', None),
               'empleado': request.form.get('empleado', ''),
               'cliente': request.form.get('celular', ''),
               'id_product': [],
               'id_sabor': [],
            }

    product_map = dict(zip(zip(products['name'], products['type']), products['product_id']))
    product_map_simple = dict(zip(products['name'], products['product_id']))

    # agrego id /Iterar sobre los productos y tipos en el carrito
    for prod, t in zip(carrito['producto'], carrito['tipo']):
        # Buscar el product_id correspondiente
        if 'Granizado' in prod or 'Michelada' in prod:
            product_id = product_map.get((prod, t))

        else:
            product_id = product_map_simple.get(prod)
        
        
        if product_id is not None:
            carrito['id_product'].append(product_id)
        else:
            print(f"Advertencia: No se encontró product_id para {prod} - {t}")
            carrito['id_product'].append(None)


    #agrego sabores
    for prod, flav in zip(carrito['producto'], carrito['sabor']):
        if 'Granizado' in prod:

            flavor_id = sabores.get('Granizados', {}).get(flav)
            carrito['id_sabor'].append(flavor_id)
        else:
            print(f"Advertencia: No se encontró flavor_id para {prod} - {flav}")
            carrito['id_sabor'].append(None)

    

    # Aquí puedes implementar la lógica de procesamiento del pago
    # Ejemplo: imprimir los datos en la consola
    print(f'''Productos: {carrito["id_product"]} {carrito["producto"]}, N° {carrito["cantidades"]}, 
          $ {carrito["precios"]}, t {carrito["tipo"]}, s {carrito["sabor"]} ''')
    
    print(f'Cliente: {carrito["cliente"]}, {carrito["empleado"]}, {carrito["tipo_pago"]}, {carrito["descuento"]}  ')



    id_pago = pago.get(carrito["tipo_pago"],None)
    id_empleado = empleados.get(carrito["empleado"],None)
    new_order = pg.get_last_pedido()
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datos_pedido = [new_order[0], id_empleado, time, id_pago, carrito["cliente"]]
    datos_detalle = [new_order[1], new_order[0], carrito["id_product"], carrito["id_sabor"] ,carrito["cantidades"],carrito["descuento"]]
    print(datos_detalle)

    send_pedido = pg.send_new_pedido(datos_pedido, datos_detalle)
    #send_pedido = 'todo ok'


    # Redirigir o mostrar una página de confirmación
    return render_template('home2.html', productos=productos, send_pedido = send_pedido)

