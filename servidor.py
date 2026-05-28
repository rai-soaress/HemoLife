from flask import Flask, render_template
from flask_cors import CORS
from extensao import bd, login_manager
import os
from dotenv import load_dotenv
from dao.usuario_dao import UsuarioDAO
from urllib.parse import quote_plus

load_dotenv()


def configurar_banco():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # PostgreSQL
    if all([db_user, db_password, db_host, db_port, db_name]):
        usuario = quote_plus(db_user)
        senha = quote_plus(db_password)
        host = quote_plus(db_host)
        banco = quote_plus(db_name)

        return (
            f"postgresql+psycopg2://"
            f"{usuario}:{senha}@{host}:{db_port}/{banco}"
        )

    # SQLite fallback
    return "sqlite:///instance/hemolife.db"


def criar_servidor():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "chave-secreta")

    app.config['SQLALCHEMY_DATABASE_URI'] = configurar_banco()

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    CORS(app)

    bd.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'usuarios.login'
    login_manager.login_message = 'Faca login para acessar esta pagina.'

    @login_manager.user_loader
    def load_user(user_id):
        return UsuarioDAO().buscar_por_id(user_id)

    # =========================
    # ROTAS
    # =========================

    @app.route('/')
    def inicio():
        return render_template('primeira_pagina.html')

    # =========================
    # ERROS
    # =========================

    @app.errorhandler(403)
    def acesso_negado(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def pagina_nao_encontrada(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def erro_interno(error):
        bd.session.rollback()
        return render_template('500.html'), 500

    # =========================
    # BLUEPRINTS
    # =========================

    from blueprints.usuario_blueprint import usuario_bp
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')

    from blueprints.ong_blueprint import bp_ong
    app.register_blueprint(bp_ong)

    from blueprints.api_blueprint import api_bp
    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    app = criar_servidor()

    with app.app_context():
        bd.create_all()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "1") == "1"
    )