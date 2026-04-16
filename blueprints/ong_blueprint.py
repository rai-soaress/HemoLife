from flask import Blueprint, request, render_template, redirect
from dao.ong_dao import OngDAO

bp_ong = Blueprint('ong', __name__, url_prefix='/ong')

dao = OngDAO()


# login
@bp_ong.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('ong_template/login.html')

    email = request.form.get('email')
    senha = request.form.get('senha')

    ong = dao.verificar_login(email, senha)

    if ong:
        return redirect('/ong/listar')

    return "Email ou senha inválidos"


# cadastro
@bp_ong.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
        return render_template('ong_template/cadastro.html')

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cnpj = request.form.get('cnpj')

    dao.cadastrar_ong(nome, email, senha, cnpj)

    return redirect('/ong/login')


# listar
@bp_ong.route('/listar')
def listar():
    ongs = dao.listar_ongs()
    return render_template('ong_template/listar.html', ongs=ongs)


# editar
@bp_ong.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    ong = dao.buscar_por_id(id)

    if request.method == 'GET':
        return render_template('ong_template/editar.html', ong=ong)

    nome = request.form.get('nome')
    email = request.form.get('email')
    cnpj = request.form.get('cnpj')

    dao.atualizar_ong(id, nome, email, cnpj)

    return redirect('/ong/listar')


# deletar
@bp_ong.route('/deletar/<int:id>')
def deletar(id):
    dao.deletar_ong(id)
    return redirect('/ong/listar')