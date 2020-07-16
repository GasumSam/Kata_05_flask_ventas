import csv, sqlite3 

filename = "./sales.csv"
database = "./data/ventas.db"

conn = sqlite3.connect(database)
cur = conn.cursor()

fSales = open(filename, 'r')
csvreader = csv.reader(fSales, delimiter=',')

headerRow = next(csvreader)
print(headerRow)

query = 'INSERT OR IGNORE INTO productos (tipo_producto, precio_unitario, coste_unitario) VALUES (?, ?, ?);'
for dataRow in csvreader:
    tupla_datos = ( dataRow[2], float(dataRow[9]), float(dataRow[10]) ) #tipo_producto | precio_unitario | coste_unitario
    cur.execute(query, tupla_datos)

conn.commit()
# conn.rollback() | cuando falla una de las grabaciones y quieres que regrese al punto de grabación anterior
conn.close()

