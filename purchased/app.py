from flask import Flask, render_template, request
from products import (productos_blueprint, productos)  # Importar el blueprint de productos
from clients import clientes_blueprint  # Importar el blueprint de clientes
from supplier import (supplier_blueprint, salidas_blueprint, gastos_blueprint)  # Importar el blueprint de supplier
import pgadmin as pg

app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(productos_blueprint)  # Registrar el blueprint de productos
app.register_blueprint(clientes_blueprint)  
app.register_blueprint(supplier_blueprint)
app.register_blueprint(salidas_blueprint)
app.register_blueprint(gastos_blueprint)

@app.route('/')
def index():
       return render_template('index.html')

@app.route('/home')
def home():
       return render_template('home2.html', productos=productos)


@app.route('/pedidos')
def pedidos():
    #df_html = pg.get_all_pedidos().to_html(classes='table table-bordered styled-table', index=False, escape=False)
    #return df_html
    try:
        df = pg.get_all_pedidos()
        if df is not None:
            df_html = df.to_html() #(classes='table table-bordered styled-table', index=True, escape=False)
            return render_template('pedidos.html', df_html=df_html)
      
        else:
            return '''<html lang="es">
                        <head>
                            <meta charset="UTF-8">
                            <title>Hola Mundo</title>
                        </head>
                        <body>
                            <h1>¡Ups! al parecer no hay datos para mostrar</h1>
                        </body>
                        </html>'''
    except ValueError as e:
        print(f'Error: {e} -- redirecting to /pedidos')
        return render_template('pedidos.html')


@app.route('/compras')
def compras():

    try:
        df = pg.get_all_compras()
        df2 = pg.get_cost_product()

        if df is not None:
            df_html1 = df[0].to_html()
            #df_html2 = df[1].to_html() #(classes='table table-bordered styled-table', index=True, escape=False)
            df_html2 = df2.to_html()
            return render_template('compras.html', df_html2=df_html2, df_html1=df_html1)
      
        else:
            return '''<html lang="es">
                        <head>
                            <meta charset="UTF-8">
                            <title>Hola Mundo</title>
                        </head>
                        <body>
                            <h1>¡Ups! al parecer no hay datos para mostrar</h1>
                        </body>
                        </html>'''
    except ValueError as e:
        print(f'Error: {e} -- redirecting to /compras')
        return render_template('compras.html')

@app.route('/*')
def reg_compras():
    compras, provs, sumins = pg.listas()
    print(compras)
    return render_template('*.html', compras=compras, provs=provs, sumins=sumins)

@app.route('/salidas')
def reg_salidas():
    _, _, sumins = pg.listas()
    print(sumins)
    return render_template('salidas.html', sumins=sumins)

@app.route('/pagos')
def reg_pagos():
    tipo_costos, ventas, gastos, renta = pg.tipo_costos()
    print(tipo_costos)
    return render_template('pagos.html', tipo_costos=tipo_costos, ventas=ventas, gastos=gastos, renta=renta)

if __name__ == '__main__':
    app.run(debug=True)
