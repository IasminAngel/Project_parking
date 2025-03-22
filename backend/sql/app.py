from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = ''

def conectar_db():
    return sqlite3.connect('crud.db')

def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS carro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano DATE
        )
        '''
    )
    conectar.commit()
    conectar.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def adicionar_carro():
    placa = request.form.get('placa')
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    ano = request.form.get('ano')

    if placa and marca and modelo and ano:
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("INSERT INTO carro (placa, marca, modelo, ano) VALUES (?, ?, ?, ?)",
                       (placa, marca, modelo, ano))
        conectar.commit()
        conectar.close()
        flash('Carro adicionado com sucesso!', 'success')
    else:
        flash('Preencha todos os campos!', 'error')

    return redirect(url_for('index'))



if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)


