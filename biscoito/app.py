from flask import Flask,render_template, request, url_for, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        return 'nome da pessoa:' + nome
    else:
        return render_template('login.html')
    
@app.route('/cor', methods=['GET'])
def cor():
    opcao = request.args.get('opcao')
    return f'Cor escolhida: {opcao}'

@app.route('/biscoito')
def biscoito():
    text = "<h1>um cookie de sessão foi definido<h1/>"
    response = make_response(text)
    response.set_cookie('primeiro_cookie','teste')
    return response

@app.route("/biscoito2", methods=['POST','GET'])
def biscoito2():
    if request.method == 'POST':
        text = "<h1>Um cookie foi definido<h1/>"
        time = int(request.form['time'])
        response = make_response(text)
        response.set_cookie('segundo_cookie', 'teste2', max_age=time)
        return response
    else:
        return render_template('biscoito2.html')
    
@app.route("/biscoito3", methods=['POST','GET'])
def biscoito3():
    option = eval(request.form['opcao'])
    template = render_template('biscoito3.html', opcao=str(bool(option)), dado='red')
    response = make_response(template)
    response.delete_cookie(request.cookies['biscoito3'])
    response.set_cookie('biscoito3', str(bool(option)), httponly=bool(option))
    return response