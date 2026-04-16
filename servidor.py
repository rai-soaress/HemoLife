from flask import Flask
from extensao import bd, login_manager
import os
from dotenv import load_dotenv
from dao.usuario_dao import UsuarioDAO

load_dotenv()

def criar_servidor():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or "chave-secreta"

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    bd.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UsuarioDAO().buscar_por_id(user_id)

    @app.route('/')
    def inicio():
        return "<h1>HemoLife</h1><a href='/usuarios/login'>Login</a>"

    from blueprints.usuario_blueprint import usuario_bp
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')

    return app


if __name__ == '__main__':
    app = criar_servidor()
    with app.app_context():
        bd.create_all()
    app.run(debug=True)