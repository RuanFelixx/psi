from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "chave_secreta"  # Importante para a segurança da sessão

# Configurando o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Define a rota de login

# Modelo de Usuário para Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Função para carregar um usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return User(id=user[0], username=user[1], password=user[2])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)  # Criptografando a senha

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash("Registro bem-sucedido! Faça login.", "success")
        except sqlite3.IntegrityError:
            flash("Nome de usuário já existe!", "danger")
        
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # Verificando a senha
            user_obj = User(id=user[0], username=user[1], password=user[2])
            login_user(user_obj)  # Faz login do usuário
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("dashboard"))

        flash("Credenciais inválidas!", "danger")

    return render_template("login.html")

@app.route("/dashboard")
@login_required  # Protege a rota
def dashboard():
    return f"Bem-vindo, {current_user.username}! <br><a href='/logout'>Sair</a>"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta!", "info")
    return redirect(url_for("login"))
