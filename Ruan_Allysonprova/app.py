from flask import Flask, render_template, request, redirect, url_for, flash
from db import db  # Importando o db do arquivo db.py
from models import Mae, Medico, Bebe, Parto
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bercario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Inicializa o db com o aplicativo Flask

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Cadastrar Mãe
@app.route('/cadastro_mae', methods=['GET', 'POST'])
def cadastro_mae():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        idade = request.form['idade']
        
        mae = Mae(nome=nome, telefone=telefone, idade=idade)
        db.session.add(mae)
        db.session.commit()
        return redirect(url_for('index'))  # Redireciona para a página inicial após o cadastro
    return render_template('cadastro_mae.html')

# Cadastrar Médico
@app.route('/cadastro_medico', methods=['GET', 'POST'])
def cadastro_medico():
    if request.method == 'POST':
        nome = request.form['nome']
        crm = request.form['crm']
        telefone = request.form['telefone']
        
        medico = Medico(nome=nome, crm=crm, telefone=telefone)
        db.session.add(medico)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro_medico.html')

@app.route('/registro_nascimento', methods=['GET', 'POST'])
def registro_nascimento():
    maes = Mae.query.all()
    medicos = Medico.query.all()

    if request.method == 'POST':
        nome_bebe = request.form['nome_bebe']
        data_nascimento = request.form['data_nascimento']
        peso = request.form['peso']
        altura = request.form['altura']
        mae_id = request.form['mae_id']
        data_parto = request.form['data_parto']
        medicos_ids = request.form.getlist('medicos')  # Obtém a lista de médicos selecionados

        # Converte as datas para objetos date
        data_nascimento_obj = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        data_parto_obj = datetime.strptime(data_parto, '%Y-%m-%d').date()

        # Verifica se pelo menos um médico foi selecionado
        if medicos_ids:  
            medico_id = medicos_ids[0]  # Pega o primeiro médico da lista
        else:
            flash("É necessário selecionar pelo menos um médico.", "error")
            return redirect(url_for('registro_nascimento'))  # Redireciona se não houver médico selecionado

        # Criando o objeto Parto com um médico associado
        parto = Parto(data_parto=data_parto_obj, medico_id=medico_id)
        db.session.add(parto)
        db.session.commit()

        # Criando o objeto Bebê e associando ao parto criado
        bebe = Bebe(
            nome=nome_bebe,
            data_nascimento=data_nascimento_obj,
            peso=peso,
            altura=altura,
            mae_id=mae_id,
            parto_id=parto.id
        )
        db.session.add(bebe)
        db.session.commit()

        # Aqui você pode associar mais médicos ao parto, se necessário
        for medico_id in medicos_ids[1:]:  # Se houver mais médicos, processa eles aqui
            pass  # Lógica para múltiplos médicos

        return redirect(url_for('index'))  # Redireciona após o cadastro

    return render_template('registro_nascimento.html', maes=maes, medicos=medicos)


# Adicione esta linha ao final de app.py
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
