import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Configurações do Flask e Flask-Login
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  # Chave secreta para a sessão

# Inicializando o Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Função de conectar com o banco de dados
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar as tabelas (se não existirem)
def create_tables():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricula TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS exercicios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    usuario_id INTEGER,
                    FOREIGN KEY (usuario_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# Função de carregar usuário
@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user['id'], user['matricula'], user['email'], user['senha'])
    return None

# Model de Usuário (não usa SQLAlchemy, mas apenas como referência)
class User(UserMixin):
    def __init__(self, id, matricula, email, senha):
        self.id = id
        self.matricula = matricula
        self.email = email
        self.senha = senha

# Página inicial (exercícios cadastrados)
@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM exercicios")
    exercicios = c.fetchall()
    conn.close()
    return render_template('exercicios.html', exercicios=exercicios)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']
        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256')  # Alterado para pbkdf2:sha256
        
        conn = get_db()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (matricula, email, senha) VALUES (?, ?, ?)", 
                      (matricula, email, hashed_password))
            conn.commit()
            flash('Cadastro realizado com sucesso!', 'success')
        except sqlite3.IntegrityError:
            flash('Matrícula ou e-mail já cadastrados!', 'danger')
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')


# Login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE matricula = ?", (matricula,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user['senha'], senha):
            user_obj = User(user['id'], user['matricula'], user['email'], user['senha'])
            login_user(user_obj)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Matrícula ou senha inválidos!', 'danger')
    return render_template('login.html')

# Logout de usuário
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado!', 'info')
    return redirect(url_for('index'))

# Cadastro de exercício (somente para usuários logados)
@app.route('/add_exercicio', methods=['GET', 'POST'])
@login_required
def add_exercicio():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO exercicios (nome, descricao, usuario_id) VALUES (?, ?, ?)", 
                  (nome, descricao, current_user.id))
        conn.commit()
        conn.close()
        flash('Exercício cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('add_exercicio.html')

if __name__ == '__main__':
    create_tables()  # Cria as tabelas do banco de dados
    app.run(debug=True)
