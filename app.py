import datetime
from services.fetch_services import (ProductFilter, StockUpdater, ProductFetcher, 
    SalesUpdate
)
from flask import Flask, jsonify, render_template, request, send_file
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook
from flask_cors import CORS
from pathlib import Path
from os import getenv
import json


load_dotenv()
report_path = Path(getenv('STATIC') + 'report.json')
spreadsheet_path = Path(getenv('STATIC') + 'pedido.xlsx')
app = Flask(__name__)
CORS(app)

@app.route("/")
def index_page():
    prods = ProductFetcher.fetch_all_prods()
    groups = ProductFetcher.fetch_all_prod_groups()
    families = ProductFetcher.fetch_all_prod_family()
    context = {'prods': prods, 'groups': groups, 'families': families}
    return render_template('index.html', **context)

@app.route("/lista_compras")
def list_compras():

    
    data = request.args.get('data', False)
    if data:
        parsed_data = json.loads(data)
    
        filtered_products = ProductFilter.filter_products(parsed_data)
    
        updated_products = StockUpdater.join_products_stock(filtered_products)
    
        result = SalesUpdate.join_product_sales(updated_products)
    
        with open(report_path, 'w+') as file:
            json.dump(result, file, indent=4)
        return jsonify({'ok': True}), 200
    else:
        return jsonify({'ok': False}), 404

@app.route("/informacoes")
def reder_list():
    if report_path.exists():
        with open(report_path, 'r') as file:
            result = json.load(file)
        return render_template('prod_list.html', products=result)
    else:
        response = {'message': 'O relatorio não foi gerado, tente novamente'}
        return jsonify(response)

@app.route("/create_spreadsheet")
def create_sheet():
    data = request.args.get('data', False)
    if data:
        parsed_data: list = json.loads(data)
        parsed_data.sort(key=lambda x: x['descricao'])
        wb = Workbook()
        sheet = wb.active
        sheet['A1'] = 'codigo'
        sheet['B1'] = 'descricao'
        sheet['C1'] = 'compra'
        sheet['D1'] = 'vl final' 
        sheet['E1'] = 'vl sugestao' 
        
        for index, item in enumerate(parsed_data, start=2):
            sheet[f'A{index}'] = item['codigo']
            sheet[f'B{index}'] = item['descricao']
            sheet[f'C{index}'] = item['compra']
            sheet[f'D{index}'] = '' 
            sheet[f'E{index}'] = '' 
        
        wb.save(spreadsheet_path)    
        return jsonify({'ok': True}), 200
    else:
        return jsonify({'ok': False}), 404

@app.route("/donwload_spreadsheet")
def donwload_spreadsheet():
    return send_file(spreadsheet_path)

@app.route("/process_sheet", methods=['POST'])
def process_sheet():
    file = request.files.get('file')
    
    if file and file.filename.endswith('.xlsx'):
        workbook = load_workbook(file)
        sheet = workbook.active
        
        data = []
        headers = [cell.value for cell in sheet[1]]
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = {}
            for header, value in zip(headers, row):
                row_data[header] = value
            data.append(row_data)
        
        return jsonify({'data': data}), 200
    else:
        return jsonify({'error': 'Arquivo inválido'}), 400

@app.route('/carregar_planilha')
def render_sheet():
    return render_template('load_sheet.html')

app.run('0.0.0.0', 5000, True)