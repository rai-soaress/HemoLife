from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from dao.usuario_dao import UsuarioDAO
from dao.ong_dao import OngDAO
from dao.inscricao_dao import InscricaoDAO

usuario_bp = Blueprint('usuarios', __name__)

dao = UsuarioDAO()

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = dao.validar_login(
            request.form.get('email'),
            request.form.get('senha')
        )

        if usuario:
            login_user(usuario)
            return redirect(url_for('usuarios.home'))

        flash('Email ou senha inválidos.')

    return render_template('login.html')


@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        sucesso, mensagem = dao.criar(
            request.form.get('nome'),
            request.form.get('email'),
            request.form.get('senha'),
            request.form.get('tipo_sanguineo'),
            request.form.get('perfil')
        )
        flash(mensagem)
        if sucesso:
            return redirect(url_for('usuarios.login'))

    return render_template('cadastro.html')


@usuario_bp.route('/home')
@login_required
def home():
    return render_template('home.html')


@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('usuarios.login'))


def acesso_admin_negado():
    flash('Acesso negado. Você precisa ser administrador para acessar esta página.')
    return redirect(url_for('usuarios.home'))


@usuario_bp.route('/admin/ongs')
@login_required
def listar_ongs():
    if current_user.perfil != 'admin':
        return acesso_admin_negado()

    ongs = OngDAO().listar_ongs()
    return render_template('admin/listar_ongs.html', ongs=ongs)


@usuario_bp.route('/admin/ongs/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_ong():
    if current_user.perfil != 'admin':
        return acesso_admin_negado()

    if request.method == 'POST':
        sucesso, mensagem = OngDAO().cadastrar_ong(
            request.form.get('nome'),
            request.form.get('email'),
            request.form.get('senha'),
            request.form.get('cnpj')
        )
        flash(mensagem)
        if sucesso:
            return redirect(url_for('usuarios.listar_ongs'))

    return render_template('admin/cadastrar_ong.html')


@usuario_bp.route('/admin/ongs/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_ong(id):
    if current_user.perfil != 'admin':
        return acesso_admin_negado()

    dao_ong = OngDAO()
    ong = dao_ong.buscar_por_id(id)

    if not ong:
        flash('ONG não encontrada.')
        return redirect(url_for('usuarios.listar_ongs'))

    if request.method == 'POST':
        sucesso, mensagem = dao_ong.atualizar_ong(
            id,
            request.form.get('nome'),
            request.form.get('email'),
            request.form.get('cnpj')
        )
        flash(mensagem)
        if sucesso:
            return redirect(url_for('usuarios.listar_ongs'))

    return render_template('admin/editar_ong.html', ong=ong)


@usuario_bp.route('/admin/ongs/deletar/<int:id>')
@login_required
def deletar_ong(id):
    if current_user.perfil != 'admin':
        return acesso_admin_negado()

    sucesso = OngDAO().deletar_ong(id)
    if sucesso:
        flash('ONG removida com sucesso.')
    else:
        flash('ONG não encontrada.')

    return redirect(url_for('usuarios.listar_ongs'))


@usuario_bp.route('/ongs')
@login_required
def ongs():
    dao_ong = OngDAO()
    dao_insc = InscricaoDAO()

    ongs = dao_ong.listar_ongs()
    inscritas = [o.id for o in ongs if dao_insc.ja_inscrito(current_user.id, o.id)]

    return render_template('ongs.html', ongs=ongs, inscritas=inscritas)


@usuario_bp.route('/ongs/inscrever/<int:id>')
@login_required
def inscrever(id):
    sucesso, mensagem = InscricaoDAO().inscrever(current_user.id, id)
    flash(mensagem)
    return redirect(url_for('usuarios.ongs'))


@usuario_bp.route('/ongs/cancelar/<int:id>')
@login_required
def cancelar(id):
    sucesso, mensagem = InscricaoDAO().cancelar(current_user.id, id)
    flash(mensagem)
    return redirect(url_for('usuarios.ongs'))


@usuario_bp.route('/minhas-ongs')
@login_required
def minhas_ongs():
    ongs = InscricaoDAO().listar_ongs_do_usuario(current_user.id)
    return render_template('minhas_ongs.html', ongs=ongs)