from flask import Flask, render_template, request
from database import db 
from models import User

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
    return render_template('listar.html')

@app.route('/listar')
def listar():
    resultado = db.session.execute(
        db.select(User)
    )
    return render_template('listar.html', resultado=resultado)