from functools import wraps

from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from dao.usuario_dao import UsuarioDAO
from dao.ong_dao import OngDAO
from dao.inscricao_dao import InscricaoDAO

usuario_bp = Blueprint('usuarios', __name__)
dao = UsuarioDAO()


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('usuarios.login'))
        if current_user.perfil != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return wrapper


@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('usuarios.home'))

    if request.method == 'POST':
        usuario = dao.validar_login(
            request.form.get('email'),
            request.form.get('senha')
        )

        if usuario:
            login_user(usuario)
            return redirect(url_for('usuarios.home'))

        flash("Email ou senha invalidos.", "error")

    return render_template('login.html')


@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return redirect(url_for('usuarios.home'))

    if request.method == 'POST':
        criado, mensagem = dao.criar(
            request.form.get('nome'),
            request.form.get('email'),
            request.form.get('senha'),
            request.form.get('tipo_sanguineo'),
            request.form.get('perfil')
        )

        if criado:
            flash(mensagem, "success")
            return redirect(url_for('usuarios.login'))

        flash(mensagem, "error")

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


@usuario_bp.route('/admin/ongs')
@login_required
@admin_required
def listar_ongs():
    ongs = OngDAO().listar_ongs()
    return render_template('admin/listar_ongs.html', ongs=ongs)


@usuario_bp.route('/admin/ongs/cadastrar', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_ong():
    if request.method == 'POST':
        criada, mensagem = OngDAO().cadastrar_ong(
            request.form.get('nome'),
            request.form.get('email'),
            request.form.get('senha'),
            request.form.get('cnpj')
        )

        if criada:
            flash(mensagem, "success")
            return redirect(url_for('usuarios.listar_ongs'))

        flash(mensagem, "error")

    return render_template('admin/cadastrar_ong.html')


@usuario_bp.route('/admin/ongs/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_ong(id):
    dao_ong = OngDAO()
    ong = dao_ong.buscar_por_id(id)
    if not ong:
        abort(404)

    if request.method == 'POST':
        atualizada, mensagem = dao_ong.atualizar_ong(
            id,
            request.form.get('nome'),
            request.form.get('email'),
            request.form.get('cnpj')
        )

        if atualizada:
            flash(mensagem, "success")
            return redirect(url_for('usuarios.listar_ongs'))

        flash(mensagem, "error")

    return render_template('admin/editar_ong.html', ong=ong)


@usuario_bp.route('/admin/ongs/deletar/<int:id>', methods=['POST'])
@login_required
@admin_required
def deletar_ong(id):
    if OngDAO().deletar_ong(id):
        flash("ONG excluida com sucesso.", "success")
    else:
        flash("ONG nao encontrada.", "error")

    return redirect(url_for('usuarios.listar_ongs'))


@usuario_bp.route('/ongs')
@login_required
def ongs():
    dao_ong = OngDAO()
    dao_insc = InscricaoDAO()

    ongs = dao_ong.listar_ongs()

    inscritas = []
    for o in ongs:
        if dao_insc.ja_inscrito(current_user.id, o.id):
            inscritas.append(o.id)

    return render_template('ongs.html', ongs=ongs, inscritas=inscritas)


@usuario_bp.route('/ongs/inscrever/<int:id>', methods=['POST'])
@login_required
def inscrever(id):
    sucesso, mensagem = InscricaoDAO().inscrever(current_user.id, id)
    flash(mensagem, "success" if sucesso else "error")

    return redirect(url_for('usuarios.ongs'))


@usuario_bp.route('/ongs/cancelar/<int:id>', methods=['POST'])
@login_required
def cancelar(id):
    sucesso, mensagem = InscricaoDAO().cancelar(current_user.id, id)
    flash(mensagem, "success" if sucesso else "error")

    return redirect(url_for('usuarios.ongs'))


@usuario_bp.route('/minhas-ongs')
@login_required
def minhas_ongs():
    ongs = InscricaoDAO().listar_ongs_do_usuario(current_user.id)
    return render_template('minhas_ongs.html', ongs=ongs)
