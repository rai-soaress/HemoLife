from functools import wraps

from flask import Blueprint, abort, jsonify, redirect, request, session, url_for
from flask_login import current_user, login_required, logout_user

from dao.inscricao_dao import InscricaoDAO
from dao.ong_dao import OngDAO

bp_ong = Blueprint('ong', __name__, url_prefix='/ong')


def get_payload():
    payload = request.get_json(silent=True)
    if payload is not None:
        return payload
    return request.form or {}


def usuario_to_dict(usuario):
    return {
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo_sanguineo': usuario.tipo_sanguineo,
    }


def ong_to_dict(ong):
    return {
        'id': ong.id,
        'nome': ong.nome,
        'email': ong.email,
        'cnpj': ong.cnpj,
        'perfil': 'ong',
    }


def ong_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ong_id = session.get('ong_id')
        if not ong_id:
            abort(401)
        ong = OngDAO().buscar_por_id(ong_id)
        if not ong:
            session.pop('ong_id', None)
            abort(401)
        return func(ong, *args, **kwargs)

    return wrapper


@bp_ong.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        payload = get_payload()
        ong = OngDAO().verificar_login(payload.get('email'), payload.get('senha'))
        if not ong:
            return jsonify({'success': False, 'message': 'Email ou senha invalidos.'}), 401

        if current_user.is_authenticated:
            logout_user()
        session['ong_id'] = ong.id
        return jsonify({'success': True, 'user': ong_to_dict(ong)})

    return redirect(url_for('usuarios.login'))


@bp_ong.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        payload = get_payload()
        criada, mensagem = OngDAO().cadastrar_ong(
            payload.get('nome'),
            payload.get('email'),
            payload.get('senha'),
            payload.get('cnpj'),
        )

        if criada:
            return jsonify({'success': True, 'message': mensagem}), 201

        return jsonify({'success': False, 'message': mensagem}), 400

    return redirect(url_for('usuarios.cadastrar'))


@bp_ong.route('/session', methods=['GET'])
def session_info():
    ong_id = session.get('ong_id')
    if not ong_id:
        return jsonify({'authenticated': False})

    ong = OngDAO().buscar_por_id(ong_id)
    if not ong:
        session.pop('ong_id', None)
        return jsonify({'authenticated': False})

    return jsonify({'authenticated': True, 'user': ong_to_dict(ong)})


@bp_ong.route('/logout', methods=['POST'])
def logout():
    session.pop('ong_id', None)
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso.'})


@bp_ong.route('/membros', methods=['GET'])
@ong_required
def membros(ong):
    usuarios = InscricaoDAO().listar_usuarios_da_ong(ong.id)
    return jsonify({
        'ong': ong_to_dict(ong),
        'membros': [usuario_to_dict(usuario) for usuario in usuarios],
    })


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
