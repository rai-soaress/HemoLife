from servidor import criar_servidor
from extensao import bd
from modelos.usuario_modelo import Usuario

app = criar_servidor()
with app.app_context():
    bd.drop_all() 
    bd.create_all()
    print("Tabelas recriadas com sucesso!")
    
    admin = Usuario("Hospital Central", "admin@hospital.com", "123", "O+", "admin")
    doador = Usuario("Samuel Doador", "samuel@teste.com", "123", "A+", "doador")
    receptor = Usuario("Sarah Receptora", "sarah@teste.com", "123", "B-", "receptor")
    
    bd.session.add_all([admin, doador, receptor])
    bd.session.commit()
    print("Dados inseridos! Agora você já pode logar no sistema.")