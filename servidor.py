from flask import Flask, jsonify, request
from flask_cors import CORS
from extensao import bd, login_manager
import os
from dotenv import load_dotenv
from dao.usuario_dao import UsuarioDAO
from modelos.exame_modelo import Exame
from modelos.inscricao_modelo import Inscricao
from modelos.ong_modelo import Ong
from modelos.unidade_modelo import Unidade
from modelos.usuario_modelo import Usuario
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

    if all([db_user, db_password, db_host, db_port, db_name]):
        usuario = quote_plus(db_user)
        senha = quote_plus(db_password)
        host = quote_plus(db_host)
        banco = quote_plus(db_name)

        return (
            f"postgresql+psycopg2://"
            f"{usuario}:{senha}@{host}:{db_port}/{banco}"
        )

    return "sqlite:///instance/hemolife.db"


def criar_servidor():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "chave-secreta")
    app.config['SQLALCHEMY_DATABASE_URI'] = configurar_banco()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_SECURE'] = False

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    frontend_origin = os.getenv("FRONTEND_URL", "http://localhost:5173")
    cors_origins = [
        frontend_origin,
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5174",
        "http://localhost:5174",
        "http://127.0.0.1:5175",
        "http://localhost:5175",
    ]
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": cors_origins}})

    bd.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'usuarios.login'
    login_manager.login_message = 'Faca login para acessar esta pagina.'

    @login_manager.user_loader
    def load_user(user_id):
        return UsuarioDAO().buscar_por_id(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"success": False, "message": "Login required"}), 401

    @app.route('/')
    def inicio():
        return jsonify({"mensagem": "Backend HemoLife funcionando com React"})

    @app.route('/api/teste')
    def teste():
        return jsonify({
            "mensagem": "Backend HemoLife funcionando com React"
        })

    def error_response(message, status):
        return jsonify({"success": False, "message": message}), status

    @app.errorhandler(403)
    def acesso_negado(error):
        return error_response('Acesso negado', 403)

    @app.errorhandler(404)
    def pagina_nao_encontrada(error):
        return error_response('Pagina nao encontrada', 404)

    @app.errorhandler(500)
    def erro_interno(error):
        bd.session.rollback()
        return jsonify({"success": False, "message": "Erro interno do servidor"}), 500

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
