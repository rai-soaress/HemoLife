from extensao import bd
from flask_login import UserMixin

class Usuario(bd.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100))
    email = bd.Column(bd.String(150), unique=True)
    senha = bd.Column(bd.String(255))
    tipo_sanguineo = bd.Column(bd.String(5))
    perfil = bd.Column(bd.String(20))

    inscricoes = bd.relationship('Inscricao', back_populates='usuario')