from flask import Flask, render_template, request, url_for
from sqlalchemy import create_engine, text 

app = Flask(__name__)

engine = create_engine("sqlite:///database.db")
connection = engine.connect() 
sql = text("""CREATE TABLE IF NOT EXISTS users(
           id INTEGER PRIMARY KEY,
           nome TEXT NOT NULL)""")
connection.execute(sql)

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        insert = text("INSERT INTO users(nome) VALUES(:nome)")
        connection.execute(insert, {'nome': nome})
        connection.commit()
        return render_template('register.html')
    else:
       return render_template('index.html')