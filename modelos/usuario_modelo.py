from extensao import bd
from flask_login import UserMixin

class Usuario(bd.Model, UserMixin): 
    __tablename__ = 'usuarios'
    
    # ESTA LINHA É A CURA PARA O ERRO DO SEU NAVEGADOR:
    __table_args__ = {'extend_existing': True} 

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False)
    email = bd.Column(bd.String(100), unique=True, nullable=False)
    senha = bd.Column(bd.String(100), nullable=False)
    tipo_sanguineo = bd.Column(bd.String(5)) # Aumentei para 5 para evitar erro com 'AB+' ou 'Desconhecido'
    perfil = bd.Column(bd.String(20)) # 'admin', 'doador' ou 'receptor'

    def __init__(self, nome, email, senha, tipo_sanguineo, perfil):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo_sanguineo = tipo_sanguineo
        self.perfil = perfil

    def __repr__(self):
        return f'<Usuario {self.nome}>'