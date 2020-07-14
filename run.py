from flask import Flask, render_template, request
import csv

app = Flask(__name__)

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

    #return #'Aquí irá un listado de países por región' + region_name

