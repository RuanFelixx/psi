from flask import Flask

app = Flask(__name__)

from produtos.produtos import produtos_blueprint
from pedidos.pedidos import pedidos_blueprint

app.register_blueprint(produtos_blueprint)
app.register_blueprint(pedidos_blueprint)