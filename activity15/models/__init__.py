"""
Modelo de datos
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurar base de datos según entorno (pruebas o normal)
if os.environ.get('TESTING'):
    # Usar base de datos en memoria para pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # Usar base de datos normal para desarrollo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)