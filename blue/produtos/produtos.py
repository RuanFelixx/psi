from flask import Blueprint, render_template

produtos_blueprint = Blueprint('produtos', __name__, template_folder='templates')


@produtos_blueprint.route('/produtos')
def produtos():
    return render_template ('produtos.html')