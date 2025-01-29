from flask import Flask, render_template, request, redirect, url_for
from models import db, Cliente, Veiculo, Locacao
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        novo_cliente = Cliente(nome=nome, email=email)
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('listar_clientes'))
    return render_template('cadastro_cliente.html')

@app.route('/cadastro_veiculo', methods=['GET', 'POST'])
def cadastro_veiculo():
    if request.method == 'POST':
        modelo = request.form['modelo']
        placa = request.form['placa']
        novo_veiculo = Veiculo(modelo=modelo, placa=placa)
        db.session.add(novo_veiculo)
        db.session.commit()
        return redirect(url_for('listar_veiculos'))
    return render_template('cadastro_veiculo.html')

@app.route('/cadastro_locacao', methods=['GET', 'POST'])
def cadastro_locacao():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        veiculo_id = request.form['veiculo_id']
        data_inicio_str = request.form['data_inicio']
        data_fim_str = request.form['data_fim']

        # Convertendo as strings para objetos de data
        data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()

        # Criando a nova locação
        nova_locacao = Locacao(
            cliente_id=cliente_id,
            veiculo_id=veiculo_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        # Salvando no banco de dados
        db.session.add(nova_locacao)
        db.session.commit()

        return redirect(url_for('listar_locacoes'))
    
    clientes = Cliente.query.all()
    veiculos = Veiculo.query.all()
    return render_template('cadastro_locacao.html', clientes=clientes, veiculos=veiculos)

@app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('listar_clientes.html', clientes=clientes)

@app.route('/veiculos')
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return render_template('listar_veiculos.html', veiculos=veiculos)

@app.route('/locacoes')
def listar_locacoes():
    locacoes = Locacao.query.all()
    return render_template('listar_locacoes.html', locacoes=locacoes)

with app.app_context():
    db.create_all()
