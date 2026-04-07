from flask import *
from extensao import bd
import os
from dotenv import load_dotenv

#força carregar o .env corretamente
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def criar_servidor():
    app = Flask(__name__)

    #pegando dados do .env
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT") or "5432"
    db_name = os.getenv("DB_NAME")

    #mostrando os dados do banco 
    print("Configurações do banco:")
    print("USER:", db_user)
    print("PORT:", db_port)
    print("HOST:", db_host)
    print("NAME:", db_name)

    #conexão com banco
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    #conectando o banco
    bd.init_app(app)

    #rota home
    @app.route('/')
    def home():
        return "HemoLife rodando!"

    return app


if __name__ == '__main__':
    try:
        app = criar_servidor()

        with app.app_context():
            print("Tentando conectar ao banco...")
            bd.create_all()
            print("Banco conectado com sucesso!")

        app.run(debug=True)

    except Exception as e:
        print("ERRO AO CONECTAR NO BANCO:")
        print(e)