from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        from dao.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo_sanguineo')
        perfil = request.form.get('perfil')
        
        if dao.criar(nome, email, senha, tipo, perfil):
            # AJUSTE: Faz o login automático para não precisar digitar a senha de novo
            usuario_recem_criado = dao.validar_login(email, senha)
            if usuario_recem_criado:
                login_user(usuario_recem_criado)
                flash("Cadastro realizado! Bem-vindo ao HemoLife.")
                return redirect(url_for('usuarios.home')) # LEVA PARA A HOME
        
        flash("Erro ao cadastrar. E-mail já existe.")
    return render_template('cadastro.html')

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from dao.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        u = dao.validar_login(request.form.get('email'), request.form.get('senha'))
        if u:
            login_user(u)
            return redirect(url_for('usuarios.home'))
        flash("E-mail ou senha incorretos.")
    return render_template('login.html')

@usuario_bp.route('/home')
@login_required
def home():
    # O current_user é passado automaticamente para o template
    return render_template('home.html')

# ROTA NOVA PARA O ADMIN CADASTRAR ONG
@usuario_bp.route('/admin/cadastrar-ong', methods=['GET', 'POST'])
@login_required
def cadastrar_ong():
    # Segurança: Apenas quem é admin acessa
    if current_user.perfil != 'admin':
        flash("Acesso restrito ao administrador!")
        return redirect(url_for('usuarios.home'))
    
    if request.method == 'POST':
        # Aqui você implementará a lógica para salvar a ONG/Hospital no banco
        flash("Unidade cadastrada com sucesso!")
        return redirect(url_for('usuarios.home'))
        
    return render_template('cadastro_ong.html')

@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('usuarios.login'))