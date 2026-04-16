from flask import *
from extensao import bd
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from modelos.usuario_modelo import Usuario 

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def criar_servidor():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or "chave-secreta-padrao"

    # Configurações do banco
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT") or "5432"
    db_name = os.getenv("DB_NAME")

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    bd.init_app(app)

    # --- CONFIGURAÇÃO DO FLASK-LOGIN ---
    login_manager = LoginManager()
    login_manager.login_view = 'usuarios.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Rota Inicial (Corrigida)
    @app.route('/')
    def home():
        return "<h1>HemoLife Rodando!</h1><br><a href='/usuarios/login'>Clique aqui para fazer Login</a>"

    # Registro da Blueprint
    from blueprints.usuario_blueprint import usuario_bp
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')

    return app

if __name__ == '__main__':
    try:
        app = criar_servidor()
        with app.app_context():
            bd.create_all()
            print("Banco conectado e tabelas verificadas!")
        app.run(port=5011, debug=True)
    except Exception as e:
        print("ERRO AO INICIAR:", e)