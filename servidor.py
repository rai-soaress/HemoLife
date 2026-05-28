from flask import Flask, render_template
from extensao import bd, login_manager
import os
from dotenv import load_dotenv
from dao.usuario_dao import UsuarioDAO
from sqlalchemy import text

load_dotenv()

def ajustar_schema():
    if bd.engine is None:
        return

    try:
        with bd.engine.begin() as conn:
            conn.execute(text('ALTER TABLE usuarios ALTER COLUMN senha TYPE VARCHAR(255)'))
            conn.execute(text('ALTER TABLE ong ALTER COLUMN senha TYPE VARCHAR(255)'))
            conn.execute(text('ALTER TABLE usuarios ALTER COLUMN email TYPE VARCHAR(150)'))
    except Exception:
        pass


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
        return render_template('primeira_pagina.html')

    from blueprints.usuario_blueprint import usuario_bp
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')

    return app


if __name__ == '__main__':
    app = criar_servidor()
    with app.app_context():
        bd.create_all()
        ajustar_schema()
    app.run(debug=True)