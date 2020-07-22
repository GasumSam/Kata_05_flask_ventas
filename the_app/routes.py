from the_app import app
from flask import render_template, request, redirect, url_for
import csv, sqlite3
from the_app.forms import ProductForm, ModProductForm

#BASE_DATOS = app.config['BASE_DATOS']

@app.route('/')
def index():
    fVentas = open(app.config['VENTAS'], 'r')
#    fVentas = open('BASE_DATOS', 'r')
    csvreader = csv.reader(fVentas, delimiter=',')

    registros =[]
    d = {}
    for linea in csvreader:
        registros.append(linea)
        if linea[0] in d:
            d[linea[0]]['ingresos'] += float(linea[11])
            d[linea[0]]['beneficios'] += float(linea[13])
        else:
            if linea[0] != 'region':
                d[linea[0]] = {'ingresos': float(linea[11]), 'beneficios': float(linea[13])}

    return render_template('region.html', ventas=d)

@app.route('/paises')
def paises():
    region_name = request.values['region']
    
    fVentas = open(app.config['VENTAS'], 'r')
    csvreader = csv.reader(fVentas, delimiter= ',')
    d = {}
    for linea in csvreader:
        if linea[0] == region_name:
            if linea[1] in d:
                d[linea[1]]['ingresos'] += float(linea[11])
                d[linea[1]]['beneficios'] += float(linea[13])
            else:
                d[linea[1]] = {'ingresos': float(linea[11]), 'beneficios': float(linea[13])}

    return render_template('pais.html', ventas_pais=d, region_nm=request.values['region'])

@app.route("/productos")
def productos():
    conn = sqlite3.connect(app.config['BASE_DATOS'])
    cur = conn.cursor()

    query = "SELECT id, tipo_producto, precio_unitario, coste_unitario FROM productos"
    productos = cur.execute(query).fetchall()  #Léemelo todo

    conn.close()
    return render_template('productos.html', productos=productos)

@app.route("/addproducto", methods=['GET', 'POST'])  #Si no ponemos nada, por defecto el método es GET
def addproduct():
    form = ProductForm(request.form)

    if request.method == 'GET':
        return render_template('newproduct.html', form = form) #me devuelves el newproduct.html vacío  | le pasamos nuestro formulario
    else:
        if form.validate():
            conn = sqlite3.connect(app.config['BASE_DATOS'])
            cur = conn.cursor()
            query = "INSERT INTO productos (tipo_producto, precio_unitario, coste_unitario) values (?, ?, ?);"
            datos = (request.values.get('tipo_producto'), request.values.get('precio_unitario'), request.values.get('coste_unitario'))

        # if datos son validos:

            cur.execute(query, datos)

            conn.commit()
            conn.close()

            return redirect(url_for("productos"))  #Ejecuta la función def productos()
        else:
            return render_template('newproduct.html', form=form)

@app.route("/modificaproducto", methods=['GET', 'POST'])
def modifica_producto():
    if request.method == 'GET':
        id = request.values.get('id')
                #name_producto = request.values['id']
    
        conn =sqlite3.connect(app.config['BASE_DATOS'])
        cur = conn.cursor()
        query = "SELECT id, tipo_producto, precio_unitario, coste_unitario FROM productos where id = ?;"

        cur.execute(query, (id,))

        fila = cur.fetchone()
        conn.close()
        if fila:
            form = ModProductForm(data={'id': fila[0], 'tipo_producto': fila[1], 'precio_unitario': fila[2], 'coste_unitario': fila[3]})
            #form.submit.label.text = "Modificar"  #Aprovecha el formulario
            return render_template('modproduct.html', form=form) 
        else:
            return redirect(url_for("productos"))
    
    else: 
        form = ModProductForm(request.form)
        if form.validate():
            if request.form.get('modificar'):
                conn = sqlite3.connect(app.config['BASE_DATOS'])
                cur = conn.cursor()

                query = 'UPDATE productos SET tipo_producto = ?, precio_unitario = ?, coste_unitario = ? WHERE id = ?;'
                try:
                    cur.execute(query, (form.tipo_producto.data, form.precio_unitario.data, form.coste_unitario.data, form.id.data ))
                    conn.commit()  #Commit antes de cerrar
                    conn.close()   #Cerrar la conexión
                except:
                    pass 
                return redirect(url_for("productos")) #Return redirect a productos
        else:          
            return render_template('modproduct.html', form=form)
    
    


