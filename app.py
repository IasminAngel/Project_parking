from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
    return render_template('index.html', carros=carros, datetime=datetime)

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

def deletar_carro(id_carro):
    try:
        conectar = conectar_db()
        cursor = conectar.cursor()

        cursor.execute("DELETE FROM carro WHERE id = ?", (id_carro,))
        conectar.commit()  

        conectar.close()

        return "Carro excluído com sucesso!"

    except Exception as e:
        return f"Erro ao excluir carro: {e}"
    
def alterar_carro(id_carro, placa, marca, modelo, ano):

    try:
        conectar = conectar_db()
        cursor = conectar.cursor()

        cursor.execute(
            "UPDATE carro SET placa = ?, marca = ?, modelo = ?, ano = ? WHERE id = ?",
            (placa, marca, modelo, ano, id_carro)
        )

        conectar.commit()  

        conectar.close()

        return "Carro alterado com sucesso!"

    except Exception as e:
        return f"Erro ao alterar o carro: {e}"


@app.route('/deletar_carro', methods=['DELETE'])
def excluir():
    dados = request.get_json()
    id_carro = dados.get('id')  

    if not id_carro:
        return jsonify({'mensagem': 'Erro: ID do carro não fornecido'}), 400

    mensagem = deletar_carro(id_carro)
    return jsonify({'mensagem': mensagem})

@app.route('/atualizar_carro', methods=['POST'])
def atualizar_carro():
    try:
        # Recebe os dados do formulário tradicional (não JSON)
        id_carro = request.form.get('id')
        placa = request.form.get('placa')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        ano = request.form.get('ano')

        if not all([id_carro, placa, marca, modelo, ano]):
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('index'))

        try:
            ano = int(ano)
            if ano < 1900 or ano > datetime.now().year:
                flash('Ano inválido!', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash('Ano deve ser um número válido!', 'error')
            return redirect(url_for('index'))

        conn = conectar_db()
        cursor = conn.cursor()
        
        # Verifica se a placa já existe em outro veículo
        cursor.execute("SELECT id FROM carro WHERE placa = ? AND id != ?", (placa, id_carro))
        if cursor.fetchone():
            flash('Esta placa já está cadastrada em outro veículo!', 'error')
            return redirect(url_for('index'))

        # Atualiza o registro
        cursor.execute(
            "UPDATE carro SET placa=?, marca=?, modelo=?, ano=? WHERE id=?",
            (placa, marca, modelo, ano, id_carro)
        )
        
        conn.commit()
        flash('Carro atualizado com sucesso!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Erro durante atualização: {str(e)}")
        flash('Erro ao atualizar carro!', 'error')
        return redirect(url_for('index'))
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
    
