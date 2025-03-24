from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


def conectar_db():
    return sqlite3.connect('crud.db')

def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS carro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL
        )
        '''
    )
    conectar.commit()
    conectar.close()

@app.route('/')
def index():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM carro")
    carros = cursor.fetchall()
    conectar.close()
    return render_template('index.html', carros=carros)

@app.route('/registrar_carro', methods=['POST'])
def adicionar_carro():
    placa = request.form.get('placa')
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    ano = request.form.get('ano')

    if placa and marca and modelo and ano:
        try:
            ano = int(ano)
            ano_atual = datetime.now().year
            if not (1900 <= ano <= ano_atual):
                flash('Ano inválido! Digite um ano entre 1900 e o ano atual.', 'error')
                return redirect(url_for('index')) 

            conectar = conectar_db()
            cursor = conectar.cursor()
            cursor.execute("INSERT INTO carro (placa, marca, modelo, ano) VALUES (?, ?, ?, ?)",
                           (placa, marca, modelo, ano))
            conectar.commit()
            conectar.close()
            flash('Carro adicionado com sucesso!', 'success')
        except sqlite3.IntegrityError:
            flash('Erro: Placa já cadastrada!', 'error')
        except Exception as e:
            flash(f'Erro ao adicionar carro: {str(e)}', 'error')
    else:
        flash('Preencha todos os campos!', 'error')
        
    return redirect(url_for('index'))

@app.route('/exibir_carro', methods=['GET'])
def exibir_carro():
    conectar = conectar_db()
    cursor = conectar.cursor()

    cursor.execute("SELECT * FROM carro")
    carros = cursor.fetchall()  

    conectar.close()

    return render_template('index.html', carros=carros)

@app.route('/deletar_carro', methods=['DEL'])
def deletar_carro():
    conectar = conectar_db()
    cursor = conectar.cursor()

    cursor.execute("DELETE FROM carro WHERE id = (?)';")
    carros = cursor.fetchall()  

    conectar.close()

    return render_template('index.html', carros=carros)


if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
    