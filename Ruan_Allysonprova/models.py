from db import db  # Importando o db do arquivo db.py
from datetime import date

# Modelo de Mãe
class Mae(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    
    # Relacionamento com os bebês
    bebês = db.relationship('Bebe', backref='mae', lazy=True)

# Modelo de Médico
class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    
    # Relacionamento com os bebês (parto)
    partos = db.relationship('Parto', backref='medico', lazy=True)

# Modelo de Bebê
class Bebe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    
    mae_id = db.Column(db.Integer, db.ForeignKey('mae.id'), nullable=False)
    parto_id = db.Column(db.Integer, db.ForeignKey('parto.id'), nullable=False)

# Modelo de Parto (relacionamento entre Bebê e Médicos)
class Parto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_parto = db.Column(db.Date, nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
