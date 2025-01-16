from flask import Flask, render_template, url_for, request, redirect
from models import User, livro 
from database import db 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    user = User(nome='mundim')
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_nome = User(nome=nome)
        db.session.add(novo_nome)
        db.session.commit()
        return redirect(url_for('index')) 
    else:
        return render_template('login.html')  


@app.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastrar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        novo_livro = livro(titulo=titulo, autor=autor)
        db.session.add(novo_livro)
        db.session.commit()
       
        return redirect(url_for('index')) 
    else:
        return render_template('cadastrar_livro.html')  
