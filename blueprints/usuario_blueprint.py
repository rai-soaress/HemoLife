from functools import wraps
import os

from flask import Blueprint, abort, request, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user

from dao.usuario_dao import UsuarioDAO
from dao.ong_dao import OngDAO
from dao.inscricao_dao import InscricaoDAO
from dao.exame_dao import ExameDAO
from dao.unidade_dao import UnidadeDAO

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


def unidade_to_dict(unidade):
    return {
        'id': unidade.id,
        'nome': unidade.nome,
        'telefone': unidade.telefone,
        'endereco': unidade.endereco,
    }


def exame_to_dict(exame):
    return {
        'id': exame.id,
        'data_exame': exame.data_exame.isoformat(),
        'horario': exame.horario,
        'status': exame.status,
        'ong': ong_to_dict(exame.ong),
        'unidade': unidade_to_dict(exame.unidade),
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


def doador_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.perfil != 'doador':
            abort(403)
        return func(*args, **kwargs)

    return wrapper


def admin_creation_allowed(payload):
    if current_user.is_authenticated and current_user.perfil == 'admin':
        return True

    codigo = os.getenv('ADMIN_REGISTRATION_CODE')
    codigo_recebido = payload.get('codigo_admin')
    return bool(codigo and codigo_recebido and codigo_recebido == codigo)


@usuario_bp.route('/session', methods=['GET'])
def session_info():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': usuario_to_dict(current_user),
        })
    ong_id = session.get('ong_id')
    if ong_id:
        ong = OngDAO().buscar_por_id(ong_id)
        if ong:
            return jsonify({
                'authenticated': True,
                'user': {
                    **ong_to_dict(ong),
                    'perfil': 'ong',
                },
            })
        session.pop('ong_id', None)
    return jsonify({'authenticated': False})


@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': usuario_to_dict(current_user),
        })

    if request.method == 'POST':
        session.pop('ong_id', None)
        payload = get_payload()
        perfil_solicitado = payload.get('perfil')
        usuario = dao.validar_login(
            payload.get('email'),
            payload.get('senha')
        )

        if usuario:
            if perfil_solicitado in ('admin', 'doador') and usuario.perfil != perfil_solicitado:
                return jsonify({
                    'success': False,
                    'message': 'Estas credenciais nao pertencem a este tipo de acesso.'
                }), 401

            login_user(usuario)
            return jsonify({
                'success': True,
                'user': usuario_to_dict(usuario),
            })

        return jsonify({'success': False, 'message': 'Email ou senha invalidos.'}), 401

    return jsonify({'authenticated': False})


@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'GET' and current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': usuario_to_dict(current_user),
        })

    if request.method == 'POST':
        payload = get_payload()
        perfil = payload.get('perfil') or 'doador'

        if perfil not in ('doador', 'admin'):
            return jsonify({
                'success': False,
                'message': 'Perfil invalido para cadastro de usuario.'
            }), 400

        if perfil == 'admin' and not admin_creation_allowed(payload):
            return jsonify({
                'success': False,
                'message': 'Informe o codigo de cadastro admin.'
            }), 403

        criado, mensagem = dao.criar(
            payload.get('nome'),
            payload.get('email'),
            payload.get('senha'),
            payload.get('tipo_sanguineo'),
            perfil
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
def logout():
    if current_user.is_authenticated:
        logout_user()
    session.pop('ong_id', None)
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
@doador_required
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
@doador_required
def inscrever(id):
    sucesso, mensagem = InscricaoDAO().inscrever(current_user.id, id)
    status = 200 if sucesso else 400
    return jsonify({'success': sucesso, 'message': mensagem}), status


@usuario_bp.route('/ongs/cancelar/<int:id>', methods=['POST'])
@login_required
@doador_required
def cancelar(id):
    sucesso, mensagem = InscricaoDAO().cancelar(current_user.id, id)
    status = 200 if sucesso else 400
    return jsonify({'success': sucesso, 'message': mensagem}), status


@usuario_bp.route('/minhas-ongs', methods=['GET'])
@login_required
@doador_required
def minhas_ongs():
    ongs = InscricaoDAO().listar_ongs_do_usuario(current_user.id)
    return jsonify({'ongs': [ong_to_dict(ong) for ong in ongs]})


@usuario_bp.route('/exames', methods=['GET'])
@login_required
@doador_required
def meus_exames():
    ongs = InscricaoDAO().listar_ongs_do_usuario(current_user.id)
    exames = ExameDAO().listar_do_usuario(current_user.id)
    unidades = UnidadeDAO().listar_unidades()
    return jsonify({
        'exames': [exame_to_dict(exame) for exame in exames],
        'ongs': [ong_to_dict(ong) for ong in ongs],
        'unidades': [unidade_to_dict(unidade) for unidade in unidades],
    })


@usuario_bp.route('/exames', methods=['POST'])
@login_required
@doador_required
def agendar_exame():
    payload = get_payload()
    sucesso, mensagem = ExameDAO().agendar(
        current_user.id,
        payload.get('ong_id'),
        payload.get('unidade_id'),
        payload.get('data_exame'),
        payload.get('horario'),
    )
    status = 201 if sucesso else 400
    return jsonify({'success': sucesso, 'message': mensagem}), status


@usuario_bp.route('/exames/<int:id>/cancelar', methods=['POST'])
@login_required
@doador_required
def cancelar_exame(id):
    sucesso, mensagem = ExameDAO().cancelar(current_user.id, id)
    status = 200 if sucesso else 404
    return jsonify({'success': sucesso, 'message': mensagem}), status
