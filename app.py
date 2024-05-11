from datetime import datetime
import json
import os
from services.fetch_services import ProductFilter, StockUpdater, ProductFetcher, SalesUpdate
from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS
from openpyxl import Workbook


app = Flask(__name__)
CORS(app)

@app.route("/")
def index_page():
    prods = ProductFetcher.fetch_all_prods()
    groups = ProductFetcher.fetch_all_prod_groups()
    families = ProductFetcher.fetch_all_prod_family()

    return render_template('index.html', prods=prods, groups=groups, families=families)

@app.route("/lista_compras")
def list_compras():
    print(datetime.now())
    data = json.loads(request.args.get('data'))
    filtered_products = ProductFilter.filter_products(data)
    print(datetime.now())

    updated_products = StockUpdater.join_products_stock(filtered_products)
    print(datetime.now())

    result = SalesUpdate.join_product_sales(updated_products)
    print(datetime.now())

    with open('data.json', 'w+') as file:
        json.dump(result, file, indent=4)
    print('done')
    return jsonify({'ok': True}), 200

@app.route("/informacoes")
def reder_list():
    with open('data.json', 'r') as file:
        result = json.load(file)
    return render_template('prod_list.html', products=result)

@app.route("/create_spreadsheet")
def create_sheet():
    data: list = json.loads(request.args.get('data'))
    data.sort(key=lambda x: x['descricao'])
    wb = Workbook()
    sheet = wb.active
    
    sheet['A1'] = 'Código'
    sheet['B1'] = 'Descrição'
    sheet['C1'] = 'Compra'
    sheet['D1'] = 'Valor final' 
    
    for index, item in enumerate(data, start=2):
        sheet[f'A{index}'] = item['codigo']
        sheet[f'B{index}'] = item['descricao']
        sheet[f'C{index}'] = item['compra']
        sheet[f'D{index}'] = '' 
    
    wb.save('cotação.xlsx')    
    return '200'

@app.route("/donwload_spreadsheet")
def donwload_spreadsheet():
    return send_file('cotação.xlsx')

app.run('0.0.0.0', 5000, True)