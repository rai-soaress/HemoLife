from extensao import bd

class Ong(bd.Model):
    __tablename__ = 'ong'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String)
    email = bd.Column(bd.String, unique=True)
    senha = bd.Column(bd.String)
    cnpj = bd.Column(bd.String, unique=True)

    membros = bd.relationship('Inscricao', back_populates='ong')