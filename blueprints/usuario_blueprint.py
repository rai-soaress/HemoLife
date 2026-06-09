from functools import wraps

from flask import Blueprint, abort, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from dao.usuario_dao import UsuarioDAO
from dao.ong_dao import OngDAO
from dao.inscricao_dao import InscricaoDAO

usuario_bp = Blueprint('usuarios', __name__)
dao = UsuarioDAO()


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
        'perfil': usuario.perfil,
        'tipo_sanguineo': usuario.tipo_sanguineo,
    }


def ong_to_dict(ong):
    return {
        'id': ong.id,
        'nome': ong.nome,
        'email': ong.email,
        'cnpj': ong.cnpj,
    }


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.perfil != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return wrapper


@usuario_bp.route('/session', methods=['GET'])
def session_info():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': usuario_to_dict(current_user),
        })
    return jsonify({'authenticated': False})


@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': usuario_to_dict(current_user),
        })

    if request.method == 'POST':
        payload = get_payload()
        usuario = dao.validar_login(
            payload.get('email'),
            payload.get('senha')
        )

        if usuario:
            login_user(usuario)
            return jsonify({
                'success': True,
                'user': usuario_to_dict(usuario),
            })

        return jsonify({'success': False, 'message': 'Email ou senha invalidos.'}), 401

    return jsonify({'authenticated': False})


@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': usuario_to_dict(current_user),
        })

    if request.method == 'POST':
        payload = get_payload()
        criado, mensagem = dao.criar(
            payload.get('nome'),
            payload.get('email'),
            payload.get('senha'),
            payload.get('tipo_sanguineo'),
            payload.get('perfil')
        )

        if criado:
            return jsonify({'success': True, 'message': mensagem}), 201

        return jsonify({'success': False, 'message': mensagem}), 400

    return jsonify({'authenticated': False})


@usuario_bp.route('/home', methods=['GET'])
@login_required
def home():
    return jsonify({
        'success': True,
        'user': usuario_to_dict(current_user),
    })


@usuario_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso.'})


@usuario_bp.route('/admin/ongs', methods=['GET'])
@login_required
@admin_required
def listar_ongs():
    ongs = OngDAO().listar_ongs()
    return jsonify([ong_to_dict(ong) for ong in ongs])


@usuario_bp.route('/admin/ongs/cadastrar', methods=['POST'])
@login_required
@admin_required
def cadastrar_ong():
    payload = get_payload()
    criada, mensagem = OngDAO().cadastrar_ong(
        payload.get('nome'),
        payload.get('email'),
        payload.get('senha'),
        payload.get('cnpj')
    )

    if criada:
        return jsonify({'success': True, 'message': mensagem}), 201

    return jsonify({'success': False, 'message': mensagem}), 400


@usuario_bp.route('/admin/ongs/<int:id>', methods=['GET', 'PUT'])
@login_required
@admin_required
def editar_ong(id):
    dao_ong = OngDAO()
    ong = dao_ong.buscar_por_id(id)
    if not ong:
        abort(404)

    if request.method == 'GET':
        return jsonify(ong_to_dict(ong))

    payload = get_payload()
    atualizada, mensagem = dao_ong.atualizar_ong(
        id,
        payload.get('nome'),
        payload.get('email'),
        payload.get('cnpj')
    )

    if atualizada:
        return jsonify({'success': True, 'message': mensagem})

    return jsonify({'success': False, 'message': mensagem}), 400


@usuario_bp.route('/admin/ongs/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def deletar_ong(id):
    if OngDAO().deletar_ong(id):
        return jsonify({'success': True, 'message': 'ONG excluida com sucesso.'})

    return jsonify({'success': False, 'message': 'ONG nao encontrada.'}), 404


@usuario_bp.route('/ongs', methods=['GET'])
@login_required
def ongs():
    dao_ong = OngDAO()
    dao_insc = InscricaoDAO()

    ongs = dao_ong.listar_ongs()
    inscritas = [o.id for o in ongs if dao_insc.ja_inscrito(current_user.id, o.id)]

    return jsonify({
        'ongs': [ong_to_dict(ong) for ong in ongs],
        'inscritas': inscritas,
    })


@usuario_bp.route('/ongs/inscrever/<int:id>', methods=['POST'])
@login_required
def inscrever(id):
    sucesso, mensagem = InscricaoDAO().inscrever(current_user.id, id)
    status = 200 if sucesso else 400
    return jsonify({'success': sucesso, 'message': mensagem}), status


@usuario_bp.route('/ongs/cancelar/<int:id>', methods=['POST'])
@login_required
def cancelar(id):
    sucesso, mensagem = InscricaoDAO().cancelar(current_user.id, id)
    status = 200 if sucesso else 400
    return jsonify({'success': sucesso, 'message': mensagem}), status


@usuario_bp.route('/minhas-ongs', methods=['GET'])
@login_required
def minhas_ongs():
    ongs = InscricaoDAO().listar_ongs_do_usuario(current_user.id)
    return jsonify({'ongs': [ong_to_dict(ong) for ong in ongs]})
