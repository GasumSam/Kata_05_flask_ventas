from flask import Flask, render_template, request, redirect, url_for
import csv, sqlite3

app = Flask(__name__)
BASE_DATOS = "./data/ventas.db"

#file = open('./sales10.csv', 'r')
#linea = file.readline()
#while linea != '':
#    registro = linea.split(',')

@app.route('/')
def index():
    fVentas = open('./sales.csv', 'r')
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
    
    fVentas = open('./sales.csv', 'r')
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
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()

    query = "SELECT id, tipo_producto, precio_unitario, coste_unitario FROM productos"
    productos = cur.execute(query).fetchall()  #Léemelo todo

    conn.close()
    return render_template('productos.html', productos=productos)

@app.route("/addproducto", methods=['GET', 'POST'])  #Si no ponemos nada, por defecto el método es GET
def addproduct():
    if request.method == 'GET':
        return render_template('newproduct.html') #me devuelves el newproduct.html vacío
    else:
        conn = sqlite3.connect(BASE_DATOS)
        cur = conn.cursor()
        query = "INSERT INTO productos (tipo_producto, precio_unitario, coste_unitario) values (?, ?, ?);"
        datos = (request.values.get('tipo_producto'), request.values.get('precio_unitario'), request.values.get('coste_unitario'))

        cur.execute(query, datos)

        conn.commit()
        conn.close()

        return redirect(url_for("productos"))  #Ejecuta la función def productos()
