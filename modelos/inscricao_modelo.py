from extensao import bd

class Inscricao(bd.Model):
    __tablename__ = 'inscricao'

    id = bd.Column(bd.Integer, primary_key=True)
    usuario_id = bd.Column(bd.Integer, bd.ForeignKey('usuarios.id'), nullable=False)
    ong_id = bd.Column(bd.Integer, bd.ForeignKey('ong.id'), nullable=False)

    usuario = bd.relationship('Usuario', back_populates='inscricoes')
    ong = bd.relationship('Ong', back_populates='membros')

    __table_args__ = (
        bd.UniqueConstraint('usuario_id', 'ong_id', name='uq_inscricao_usuario_ong'),
    )
