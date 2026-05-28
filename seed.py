from servidor import criar_servidor
from extensao import bd
from modelos.usuario_modelo import Usuario
from modelos.ong_modelo import Ong
from modelos.unidade_modelo import Unidade
from werkzeug.security import generate_password_hash

app = criar_servidor()
with app.app_context():
    bd.drop_all() 
    bd.create_all()
    print("Tabelas recriadas com sucesso!")
    
    admin = Usuario(
        nome="Hospital Central",
        email="admin@hospital.com",
        senha=generate_password_hash("123"),
        tipo_sanguineo=None,
        perfil="admin",
    )
    doador = Usuario(
        nome="Samuel Doador",
        email="samuel@teste.com",
        senha=generate_password_hash("123"),
        tipo_sanguineo="A+",
        perfil="doador",
    )
    ong = Ong(
        nome="Hemo ONG",
        email="ong@teste.com",
        senha=generate_password_hash("123"),
        cnpj="00.000.000/0001-00",
    )
    unidade = Unidade(
        nome="Hospital de Ipaumirim",
        telefone="(88) 99999-9999",
        endereco="Centro",
    )
    
    bd.session.add_all([admin, doador, ong, unidade])
    bd.session.commit()
    print("Dados inseridos! Admin: admin@hospital.com / 123 | Doador: samuel@teste.com / 123")
