from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Book  # Importando os modelos do arquivo models.py

# Inicialização do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'seu_segredo_aqui'  # Alterar para algo seguro
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Usando SQLite como banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db.init_app(app)

# Inicialização do LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Página de login

with app.app_context():
    db.create_all()

# Carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota de index (página inicial)
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)  # Realiza o login do usuário
            return redirect(url_for('index'))  # Redireciona após login bem-sucedido
        else:
            return 'Invalid email or password'

    return render_template('login.html')

# Rota de logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Verifica se o email já está registrado
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            # Aqui você pode tratar o erro como quiser (exibir uma mensagem, etc.)
            return "Email já registrado. Por favor, tente outro."

        user = User(name=name, email=email)
        user.set_password(password)  # Assumindo que você tenha um método set_password
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Rota de adicionar livro
@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        book = Book(title=title, author=author)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_book.html')

@app.route('/list_books')
@login_required
def list_books():
    books = Book.query.all()  # Utilize o nome correto da classe aqui
    return render_template('books.html', books=books)


# Rota de detalhes de um livro
@app.route('/book/<int:book_id>')
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)  # Recupera o livro pelo ID
    return render_template('book_details.html', book=book)


# Rodando o servidor
if __name__ == '__main__':
    app.run(debug=True)
