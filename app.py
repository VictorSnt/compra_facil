import json
import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from services.fetch_services import ProductFilter, StockUpdater, ProductFetcher, SalesUpdate


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
    print('init')
    data = json.loads(request.args.get('data'))
    filtered_products = ProductFilter.filter_products(data)
    updated_products = StockUpdater.join_products_stock(filtered_products)
    result = SalesUpdate.join_product_sales(updated_products)
    print(result)
    with open('data.json', 'w+') as file:
        json.dump(result, file, indent=4)
    print('done')
    return jsonify({'ok': True}), 200

@app.route("/informacoes")
def reder_list():
    with open('data.json', 'r') as file:
        result = json.load(file)
    return render_template('prod_list.html', products=result)

app.run('0.0.0.0', 5000, True)