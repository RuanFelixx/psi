from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Book ,Exercicio, Produto


app = Flask(__name__)
app.config['SECRET_KEY'] = 'seu_segredo_aqui'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'  

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
            login_user(user)  
            return redirect(url_for('index'))  
        else:
            return 'Invalid email or password'

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return "Email já registrado. Por favor, tente outro."

        user = User(name=name, email=email)
        user.set_password(password)  
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


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
    books = Book.query.all()  
    return render_template('books.html', books=books)

@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)  
    db.session.delete(book) 
    db.session.commit() 
    

    return redirect(url_for('list_books'))



@app.route('/add_exercicio', methods=['GET', 'POST'])
@login_required
def add_exercicio():
    if request.method == 'POST':
        nome_exercicio = request.form.get('exercicio')
        if nome_exercicio:  
            novo_exercicio = Exercicio(nome=nome_exercicio)
            db.session.add(novo_exercicio)
            db.session.commit()
            return redirect(url_for('index'))
    
    return render_template('add_exercicio.html')  

@app.route('/list_exercicios')
@login_required
def list_exercicios():
    exercicios = Exercicio.query.all()  
    return render_template('exercicios.html', exercicios=exercicios)


@app.route('/delete_exercicio/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_exercicio(id):
    exercicio = Exercicio.query.get_or_404(id)

    db.session.delete(exercicio)
    db.session.commit()

    return redirect(url_for('list_exercicios'))


@app.route('/add_produto', methods=['GET', 'POST'])
@login_required
def add_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        
        novo_produto = Produto(nome=nome, descricao=descricao, preco=preco)
        db.session.add(novo_produto)
        db.session.commit()
        
        return redirect(url_for('list_produtos'))
    
    return render_template('add_produto.html')


@app.route('/list_produtos')
@login_required
def list_produtos():
    produtos = Produto.query.all()
    return render_template('list_produtos.html', produtos=produtos)

@app.route('/delete_produto/<int:id>')
@login_required
def delete_produto(id):
    produto = Produto.query.get(id)
    
    if produto:
        db.session.delete(produto)
        db.session.commit()
    
    return redirect(url_for('list_produtos'))



if __name__ == '__main__':
    app.run(debug=True)
