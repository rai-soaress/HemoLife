from extensao import bd

class Ong(bd.Model):
    __tablename__ = 'ong'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(120), nullable=False)
    email = bd.Column(bd.String(120), unique=True, nullable=False)
    senha = bd.Column(bd.String(255), nullable=False)
    cnpj = bd.Column(bd.String(30), unique=True, nullable=False)

    membros = bd.relationship(
        'Inscricao',
        back_populates='ong',
        cascade='all, delete-orphan',
    )
