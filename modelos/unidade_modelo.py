from extensao import bd


class Unidade(bd.Model):
    __tablename__ = 'unidades'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False)
    telefone = bd.Column(bd.String(20), nullable=False)
    endereco = bd.Column(bd.String(150), nullable=False)
