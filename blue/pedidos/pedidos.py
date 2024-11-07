from flask import Blueprint, render_template

pedidos_blueprint = Blueprint('pedidos', __name__, template_folder='templates')


@pedidos_blueprint.route('/pedidos')
def produtos():
    return render_template ('pedidos.html')