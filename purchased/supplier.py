import os
import sys
from flask import Blueprint, render_template, request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pgadmin as pg

# Crear el blueprint para clientes
supplier_blueprint = Blueprint('registros', __name__)

# Ruta para consultar y agregar clientes
@supplier_blueprint.route('/registros', methods=['POST'])
def registros():
    compras, provs, sumins = pg.listas()

    agregar_prov = 'crear_proveedor' in request.form
    agregar_sum = 'crear_suministro' in request.form
    agregar_com = 'crear_compra' in request.form
    agregar_detail = 'crear_detalle' in request.form
    
    if agregar_prov:
        # Obtener los datos del nuevo cliente
        new_local = request.form.get('local_name', '')
        new_contact = request.form.get('contact_name', '')
        new_cel = request.form.get('celular', '')
        new_address = request.form.get('direccion', '')
        
        # Crear un array con los datos del nuevo cliente
        nuevo_proveedor = [new_local, new_contact, new_cel, new_address]

        print(f"Nuevo cliente: {nuevo_proveedor}")
        # Insertar el nuevo cliente en la base de datos
        resultado = pg.new_supplier(nuevo_proveedor)

    elif agregar_sum:
        # Obtener los datos del nuevo cliente
        new_product = request.form.get('product', '')
        new_type = request.form.get('type', '')
        new_medida = request.form.get('medida', '')
        new_udMedida = request.form.get('ud_medida', '')
        
        # Crear un array con los datos del nuevo cliente
        nuevo_suminsitro = [new_product, new_type, new_medida, new_udMedida]

        print(f"Nuevo cliente: {nuevo_suminsitro}")
        # Insertar el nuevo cliente en la base de datos
        resultado = pg.new_inventory(nuevo_suminsitro)

    elif agregar_com:
        # Obtener los datos del nuevo cliente
        new_factura = request.form.get('factura', '')
        new_prov = request.form.get('id_supplier', '')

        
        # Crear un array con los datos del nuevo cliente
        nueva_compra = [new_factura, new_prov]

        print(f"Nuevo factura compra: {nueva_compra}")
        # Insertar el nuevo cliente en la base de datos
        resultado = pg.new_compra(nueva_compra)

    elif agregar_detail:
        d_compras = {'factura': request.form.get('id_compra', ''),
                    'suministro': request.form.getlist('suministro_pro'),
                   'cantidad': request.form.getlist('quantity'),
                   'precio': request.form.getlist('price_c'),
                   }
        
        id_suministro = [int(item.split(' ')[0]) for item in d_compras['suministro']]

        send_detalles = [d_compras['factura'], id_suministro, d_compras['cantidad'], d_compras['precio']]

        resultado = pg.send_new_detail_compra(send_detalles)
        
    return render_template('*.html', resultado=resultado, compras=compras, provs=provs, sumins=sumins)

# Crear el blueprint para clientes
salidas_blueprint = Blueprint('inv_salidas', __name__)

# Ruta para consultar y agregar clientes
@supplier_blueprint.route('/inv_salidas', methods=['POST'])
def inv_salidas():
    _, _, sumins = pg.listas()

    agregar_salida = 'crear_salida' in request.form
    if agregar_salida:
        d_salida = {'inventario': request.form.getlist('inventario_pro'),
                'cantidad': request.form.getlist('quantity_inv')}
        
        id_inv = [int(item.split(' ')[0]) for item in d_salida['inventario']]
        send_salidas = [id_inv, d_salida['cantidad']]
        print(send_salidas)

        resultado = pg.send_new_inv_salida(send_salidas)

    return render_template('salidas.html', resultado=resultado, sumins=sumins)

# Crear el blueprint para clientes
gastos_blueprint = Blueprint('gastos', __name__)

# Ruta para consultar y agregar gastos
@supplier_blueprint.route('/gastos', methods=['POST'])
def gastos():
    tipo_costos, ventas, gastos, renta = pg.tipo_costos()

    agregar_salida = 'crear_salida' in request.form
    if agregar_salida:
        d_salida = {'ref': request.form.getlist('ref_tipos'),
                    'valor': request.form.getlist('valor_salida'),
                'detalle': request.form.getlist('detalles')}
        
        id_ref = [int(item.split(' ')[0]) for item in d_salida['ref']]
        send_gasto = [d_salida['valor'], d_salida['detalle'], id_ref]
        print(send_gasto)

        resultado = pg.send_new_salida_gasto(send_gasto)

    return render_template('pagos.html',
        resultado=resultado,
        tipo_costos=tipo_costos,
        ventas=ventas,
        gastos=gastos,
        renta=renta)