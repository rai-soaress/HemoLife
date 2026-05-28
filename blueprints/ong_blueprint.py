from flask import Blueprint, redirect, url_for
from flask_login import login_required

bp_ong = Blueprint('ong', __name__, url_prefix='/ong')


@bp_ong.route('/login')
def login():
    return redirect(url_for('usuarios.login'))


@bp_ong.route('/cadastrar')
@login_required
def cadastrar():
    return redirect(url_for('usuarios.cadastrar_ong'))


@bp_ong.route('/listar')
@login_required
def listar():
    return redirect(url_for('usuarios.listar_ongs'))


@bp_ong.route('/editar/<int:id>')
@login_required
def editar(id):
    return redirect(url_for('usuarios.editar_ong', id=id))


@bp_ong.route('/deletar/<int:id>', methods=['POST'])
@login_required
def deletar(id):
    return redirect(url_for('usuarios.deletar_ong', id=id), code=307)
