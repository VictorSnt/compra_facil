from flask import Flask, render_template
from services.fetch_services import (
    fetch_all_prods,
    fetch_all_prod_groups,
    fetch_all_prod_family
)

app = Flask(__name__)

@app.route("/")
def index_page():
    prods = fetch_all_prods()
    groups = fetch_all_prod_groups()
    families = fetch_all_prod_family()

    return render_template('index.html', prods=prods, groups=groups, families=families)
