from flask import Flask, session, request, render_template, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = 'database.db'

app.config['SECRET_KEY'] = 'superdificil'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, nome):
        self.id = nome


bancodados = {}

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dash():
    return render_template('dashboard.html', nome=current_user.id)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))

    if request.method == 'GET':
        return render_template('login.html')
    else:
        nome = request.form['nome']
        senha = request.form['senha']

        if nome in bancodados and check_password_hash(bancodados[nome], senha):
            user = User(nome)
            login_user(user)  
            return redirect(url_for('dash'))
        else:
            return "SENHA INCORRETA ou não está cadastrado"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

      
        hashed_senha = generate_password_hash(senha)

        with get_connection() as conn:
            try:
                conn.execute('INSERT INTO users (nome, senha) VALUES (?, ?)', (nome, hashed_senha))
                bancodados[nome] = hashed_senha  
                user = User(nome)
                login_user(user)  
                return redirect(url_for('dash'))
            except sqlite3.IntegrityError:
                return "Usuário já cadastrado."

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  
    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    nome = current_user.id  

    with get_connection() as conn:
        conn.execute('DELETE FROM users WHERE nome = ?', (nome,))
        
        if nome in bancodados:
            del bancodados[nome]
        
        logout_user()  
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)