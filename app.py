import json
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from services.fetch_services import (
    fetch_all_prods,
    fetch_all_prod_groups,
    fetch_all_prod_family,
    filter_products
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def index_page():
    prods = fetch_all_prods()
    groups = fetch_all_prod_groups()
    families = fetch_all_prod_family()

    return render_template('index.html', prods=prods, groups=groups, families=families)

@app.route("/lista_compras")
def list_compras():

    data = json.loads(request.args.get('data'))
    
    response = filter_products(data)
    print(response)
    return jsonify({'mensagem': 'Dados recebidos com sucesso'}), 200
    
app.run('127.0.0.1', 5000, True)