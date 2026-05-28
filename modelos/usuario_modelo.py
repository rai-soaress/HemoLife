from extensao import bd
from flask_login import UserMixin

class Usuario(bd.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False)
    email = bd.Column(bd.String(120), unique=True, nullable=False)
    senha = bd.Column(bd.String(255), nullable=False)
    tipo_sanguineo = bd.Column(bd.String(5))
    perfil = bd.Column(bd.String(20), nullable=False, default='doador')

    inscricoes = bd.relationship(
        'Inscricao',
        back_populates='usuario',
        cascade='all, delete-orphan',
    )
