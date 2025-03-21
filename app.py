from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import redirect


app = Flask(__name__)
app.secret_key = ''

def conectar_db():
    conectar = sqlite3.connect('crud.db')
    return conectar

def criar_tabela():
    conectar = conectar_db()
    cursor = conectar_cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS carro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano DATE
        
        )
        ''')

        conectar.commit()
        conectar.close()

        @app.route('/')
        def index():
            return render_template ('index.html')
        
        @app.route ('' methods ('POST'))