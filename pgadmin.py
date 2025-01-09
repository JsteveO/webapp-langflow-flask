import psycopg2
import pandas as pd
from datetime import datetime
import traceback
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)


print("Hola Mundito")

def data_connection():
    # Datos de conexión
    conexion = psycopg2.connect(
        host="192.168.192.1",  # Cambia por la IP correcta de tu servidor PostgreSQL
        database="Interior_505",
        user="postgres",
        password="stivenolano",
        port="5432"
    )

    return conexion

def get_client(celphone):
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL
        cursor.execute('''SELECT * FROM clientes AS cl
                    JOIN membresia AS mb
                    ON mb.customer_id = cl.customer_id
                    WHERE cl.phone = %s''', (celphone,))  # Usar %s como placeholder y pasar el valor de 'celphone''

        # Obtener los resultados de la consulta
        datos = cursor.fetchall()

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Cerrar la conexión
        cursor.close()
        conexion.close()

        # Crear un DataFrame de pandas con los datos obtenidos
        df = pd.DataFrame(datos, columns=columnas)

    except Exception as e:
        # En caso de error, podrías querer registrar el error o manejarlo
        print(f"Error al obtener el cliente: {e}")
        df = pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

    finally:
        # Cerrar la conexión, si está abierta
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return df

def new_client(data_client):
    conexion = data_connection()
    cursor = None
    try:
        cursor = conexion.cursor()
        # Ejecutar un insert SQL
        cursor.execute('''INSERT INTO public.clientes(
                        customer_id, first_name, phone, address)
                        VALUES (%s, %s, %s, %s);''',
                       (data_client[0], data_client[1], data_client[0], data_client[2]))
        # Confirmar los cambios en la base de datos
        conexion.commit()
        return f"Cliente {data_client[1]} agregado. ID: {data_client[0]}"  # Mensaje de éxito

    except Exception as e:
        # Manejo de errores
        print(f"Error al insertar cliente: {e}")
        return "Error al agregar cliente"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def get_products():
    
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL
        cursor.execute('''SELECT * FROM public.productos AS pp
                       JOIN public.categoria as cc
                       ON cc.category_id = pp.category_id;''')

        # Obtener los resultados de la consulta
        datos = cursor.fetchall()

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Cerrar la conexión
        cursor.close()
        conexion.close()

        # Crear un DataFrame de pandas con los datos obtenidos
        df = pd.DataFrame(datos, columns=columnas)

    except Exception as e:
        # En caso de error, podrías querer registrar el error o manejarlo
        print(f"Error al obtener el cliente: {e}")
        df = pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

    finally:
        # Cerrar la conexión, si está abierta
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return df

def get_last_pedido():
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        
        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT COALESCE(MAX(order_id), 0) FROM public.pedidos''')
        new_order = cursor.fetchone()[0] + 1

        # Ejecutar una consulta SQL para detalles de pedidos
        cursor.execute('''SELECT COALESCE(MAX(order_detail_id), 0) FROM public.detalle_pedidos''')
        new_detail = cursor.fetchone()[0] + 1

        return new_order, new_detail

    except Exception as e:
        print(f"Error al obtener el último pedido: {e}")
        return None, None
    finally:
        # Cerrar el cursor y la conexión, si están abiertos
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def send_new_pedido(send_order, send_detalles):
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL
        cursor.execute('''INSERT INTO public.pedidos(
                       order_id, employee_id, order_date, id_pago, customer_id)
                       VALUES (%s, %s, %s, %s, %s);''',
                       (send_order))

        detail_order_id, order_id, product_ids, flavors_id, quantities, discounts = send_detalles

        for product_id, flavor_id, quantity in zip(product_ids, flavors_id, quantities):
            cursor.execute('''
                INSERT INTO public.detalle_pedidos(order_detail_id, order_id, product_id, flavor_id, quantity, id_descuento)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (detail_order_id, order_id, product_id, flavor_id, int(quantity), discounts))
            detail_order_id += 1  # Incrementar para el siguiente detalle

         # Confirmar los cambios en la base de datos
        conexion.commit()
        return f"Pedido {send_order[0]} agregado para {send_order[4]}"  # Mensaje de éxito

    except Exception as e:
        if conexion:
            conexion.rollback()
        print(f"Error al insertar Pedido y detalles: {e}")
        return "Error al agregar Pedido y detalles"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def get_all_pedidos():
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        
        # Ejecutar una consulta SQL para pedidos
        '''cursor.execute(SELECT dp.status, pp.order_id, pp.customer_id, pr.name, sb.flavor, dp.quantity, dp.price, (de.descuento*100) AS "%" FROM detalle_pedidos AS dp
                        LEFT JOIN pedidos AS pp
                        ON dp.order_id = pp.order_id
                        LEFT JOIN productos AS pr
                        ON dp.product_id = pr.product_id
                        LEFT JOIN sabores AS sb
                        ON dp.flavor_id = sb.flavor_id
                        LEFT JOIN descuentos AS de
                        ON dp.id_descuento = de.id_descuento
                        ORDER BY pp DESC)'''
        
        cursor.execute('''SELECT * FROM productos ORDER BY product_id ASC;''')


        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        # Crear un DataFrame de pandas con los datos obtenidos
        df = pd.DataFrame(datos, columns=columnas)

        return df

    except Exception as e:
        print(f"Error al obtener los pedidos: {e}")
        return None, None
    finally:
        # Cerrar el cursor y la conexión, si están abiertos
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def get_all_compras():
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()

        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT cm.purchase_date, cm.purchase_id, pv.name_local, SUM(dc.price) AS total_price
                    FROM detalle_compras AS dc
                    LEFT JOIN compras AS cm
                    ON cm.purchase_id = dc.purchase_id
                    LEFT JOIN proveedor AS pv
                    ON pv.supplier_id = cm.supplier_id
                    GROUP BY cm.purchase_id, pv.supplier_id
                    ORDER BY cm.purchase_date DESC;''')

        total = cursor.fetchall()
        columnas1 = [desc[0] for desc in cursor.description]

        # Crear un DataFrame de pandas con los datos obtenidos
        df1 = pd.DataFrame(total, columns=columnas1)
        
        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT cm.purchase_date, cm.purchase_id, dc.quantity, sm.product, dc.price FROM detalle_compras AS dc
                        LEFT JOIN compras AS cm
                        ON cm.purchase_id = dc.purchase_id
                        LEFT JOIN suministros AS sm
                        ON dc.supply_id = sm.inventory_id
                        ORDER BY cm.purchase_date DESC''')

        datos = cursor.fetchall()
        columnas2 = [desc[0] for desc in cursor.description]

        # Crear un DataFrame de pandas con los datos obtenidos
        df2 = pd.DataFrame(datos, columns=columnas2)

        return df1, df2

    except Exception as e:
        print(f"Error al obtener los pedidos: {e}")
        return None, None
    finally:
        # Cerrar el cursor y la conexión, si están abiertos
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def new_supplier(data_supplier):
    conexion = data_connection()
    cursor = None
    try:
        cursor = conexion.cursor()

        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT COALESCE(MAX(supplier_id), 0) FROM public.proveedor''')
        new_supplier = cursor.fetchone()[0] + 1


        # Ejecutar un insert SQL
        cursor.execute('''INSERT INTO public.proveedor(
                        supplier_id, name_local, contact_name, phone, address)
                        VALUES (%s, %s, %s, %s, %s);''',
                       (new_supplier, data_supplier[0], data_supplier[1], data_supplier[2], data_supplier[3]))
        # Confirmar los cambios en la base de datos
        conexion.commit()
        return f"Proveedor {data_supplier[0]} agregado. ID: {new_supplier}"  # Mensaje de éxito

    except Exception as e:
        # Manejo de errores
        print(f"Error al insertar proveedor: {e}")
        return "Error al agregar proveedor"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def new_inventory(data_suminsitro):
    conexion = data_connection()
    cursor = None
    try:
        cursor = conexion.cursor()

        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT COALESCE(MAX(inventory_id), 0) FROM public.suministros''')
        new_inventory = cursor.fetchone()[0] + 1


        # Ejecutar un insert SQL
        cursor.execute('''INSERT INTO public.suministros(
                        inventory_id, product, type_inventory, measurement, unit_quantity)
                        VALUES (%s, %s, %s, %s, %s);''',
                       (new_inventory, data_suminsitro[0], data_suminsitro[1], data_suminsitro[2], data_suminsitro[3]))
        # Confirmar los cambios en la base de datos
        conexion.commit()
        return f"Suministro {data_suminsitro[0]} agregado. ID: {new_inventory}"  # Mensaje de éxito

    except Exception as e:
        # Manejo de errores
        print(f"Error al insertar inventario: {e}")
        return "Error al agregar inventario"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def new_compra(data_compra):
    conexion = data_connection()
    cursor = None
    try:
        cursor = conexion.cursor()

        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT supplier_id FROM public.proveedor
                       WHERE name_local = %s''', (data_compra[1],))
        prov = cursor.fetchone()[0]


        # Ejecutar un insert SQL
        cursor.execute('''INSERT INTO public.compras(
                        purchase_id, supplier_id, purchase_date)
                        VALUES (%s, %s, %s);''',
                       (data_compra[0], prov, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        # Confirmar los cambios en la base de datos
        conexion.commit()
        return f"Factura {data_compra[0]} agregado."  # Mensaje de éxito

    except Exception as e:
        # Manejo de errores
        print(f"Error al insertar proveedor: {e}")
        return "Error al agregar proveedor"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def send_new_detail_compra(send_detalles):
    conexion = None
    cursor = None
    try:
        # Validar los datos
        '''if not send_detalles or len(send_detalles) != 4:
            return "Datos inválidos para agregar factura y detalles"'''
        
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL
        cursor.execute('''SELECT COALESCE(MAX(purchase_detail_id), 0) FROM public.detalle_compras''')
        purchase_detail_ids = cursor.fetchone()[0] + 1

        purchase_id, supply_ids, quantitys, prices = send_detalles

        for supply_id, quantity, price in zip(supply_ids, quantitys, prices):
            cursor.execute('''
                INSERT INTO public.detalle_compras(purchase_detail_id, purchase_id, supply_id, quantity, price)
                VALUES (%s, %s, %s, %s, %s)
            ''', (purchase_detail_ids, purchase_id, supply_id, quantity, price))
            purchase_detail_ids += 1  # Incrementar para el siguiente detalle


        #ingresar salida de dinero en salidas_ventas______________________________________________
            #valor total de la compra
        cursor.execute('''SELECT SUM(price) FROM detalle_compras 
                       WHERE purchase_id = %s;''',(purchase_id,))
        valor = cursor.fetchone()[0]

            #factura
        cursor.execute('''SELECT COALESCE(MAX(id_salidas), 0) FROM public.salidas_ventas''')
        id_salidas = cursor.fetchone()[0] + 1

        cursor.execute('''
                INSERT INTO public.salidas_ventas(id_salidas, valor_salida, descripcion, id_ref, id_purchase, last_update)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (id_salidas, valor, 'compra insumos', 1, purchase_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Confirmar los cambios en la base de datos
        conexion.commit()

        return f"Detalles de factura {purchase_id} agregado. Valor: {valor}"  # Mensaje de éxito

    except Exception as e:
        if conexion:
            conexion.rollback()
        print(f"Error al insertar factura y detalles: {e}")
        print(traceback.format_exc())
        return "Error al agregar factura y detalles"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def listas():
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()

        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT purchase_id FROM compras
                        ORDER BY purchase_date DESC
                        LIMIT 10;''')
        array_compras = cursor.fetchall()
        compras = [fila[0] for fila in array_compras]

        cursor.execute('''SELECT name_local FROM proveedor;''')
        array_prov = cursor.fetchall()
        provs = [fila[0] for fila in array_prov]

        cursor.execute('''SELECT concat(inventory_id,' - ',product) FROM suministros
                        ORDER BY inventory_id ASC;''')
        array_sumin = cursor.fetchall()
        sumins = [fila[0] for fila in array_sumin]

        
        return compras, provs, sumins

    except Exception as e:
        print(f"Error al obtener los pedidos: {e}")
        return None, None
    finally:
        # Cerrar el cursor y la conexión, si están abiertos
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def get_cost_product():
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        
        # Ejecutar una consulta SQL para pedidos
        cursor.execute('''SELECT ps.supply_id, pp.name, ps.flavor_id, ss.product, ps.quantity, (ps.quantity * ss.unit_cost) AS costo FROM productos_suministros AS ps
                        JOIN productos AS pp ON pp.product_id = ps.product_id
                        JOIN suministros AS ss ON ss.inventory_id = ps.inventory_id
                        WHERE ps.product_id = 14''')

        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        # Crear un DataFrame de pandas con los datos obtenidos
        df = pd.DataFrame(datos, columns=columnas)

        return df

    except Exception as e:
        print(f"Error al obtener los pedidos: {e}")
        return None, None
    finally:
        # Cerrar el cursor y la conexión, si están abiertos
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def send_new_inv_salida(send_salidas):
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL
        cursor.execute('''SELECT COALESCE(MAX(salidas_id), 0) FROM public.inventario_ajustes''')
        salidas_ids = cursor.fetchone()[0] + 1
        print(salidas_ids)

        inventario_ids, quantitys = send_salidas

        for inventario_id, quantity in zip(inventario_ids, quantitys):
            cursor.execute('''
                INSERT INTO public.inventario_ajustes(salidas_id, inventory_id, quantity, last_update)
                VALUES (%s, %s, %s, %s)
            ''', (salidas_ids, inventario_id, quantity, datetime.now().strftime("%Y-%m-%d")))
            salidas_ids += 1  # Incrementar para el siguiente detalle

         # Confirmar los cambios en la base de datos
        conexion.commit()
        return f"Detalles de salidas {salidas_ids - 1} agregado"  # Mensaje de éxito

    except Exception as e:
        if conexion:
            conexion.rollback()
        print(f"Error al insertar salida y detalles: {e}")
        return "Error al agregar salida y detalles"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def tipo_costos():
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()

        cursor.execute('''SELECT SUM(ventas) FROM ventas''')
        ventas = cursor.fetchone()[0] + 1

        cursor.execute('''SELECT SUM(valor_salida) FROM salidas_ventas''')
        gastos = cursor.fetchone()[0] + 1

        # Ejecutar una consulta SQL para tipo_costos
        cursor.execute('''SELECT concat(id_ref_cost,' - ',name) FROM tipo_costo
                        ORDER BY id_ref_cost ASC;''')
        
        array_cost = cursor.fetchall()
        tipo_costos = [fila[0] for fila in array_cost]

        renta = ventas -gastos
        ventas, gastos, renta = ("${:,.2f}".format(i) for i in (ventas, gastos, renta))
        
        return tipo_costos, ventas, gastos, renta

    except Exception as e:
        print(f"Error al obtener los pedidos: {e}")
        return None, None
    finally:
        # Cerrar el cursor y la conexión, si están abiertos
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def send_new_salida_gasto(send_gasto):
    conexion = None
    cursor = None
    try:
        # Datos de conexión
        conexion = data_connection()

        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL
        cursor.execute('''SELECT COALESCE(MAX(id_salidas), 0) FROM public.salidas_ventas''')
        id_salidas = cursor.fetchone()[0] + 1
        valor_total = 0

        print(id_salidas)

        valor_salidas, detalles, id_refs = send_gasto

        for valor_salida, detalle, id_ref in zip(valor_salidas, detalles, id_refs):
            cursor.execute('''
                INSERT INTO public.salidas_ventas(id_salidas, valor_salida, descripcion, id_ref, last_update)
                VALUES (%s, %s, %s, %s, %s)
            ''', (id_salidas, valor_salida, detalle, id_ref, datetime.now().strftime("%Y-%m-%d")))
            id_salidas += 1  # Incrementar para el siguiente detalle
            valor_total += int(valor_salida)

         # Confirmar los cambios en la base de datos
        conexion.commit()
        return f"Detalles de gastos {id_salidas - 1} agregado, total: {valor_total}"  # Mensaje de éxito

    except Exception as e:
        if conexion:
            conexion.rollback()
        print(f"Error al insertar salida y detalles: {e}")
        return "Error al agregar salida y detalles"

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()