from datetime import datetime

from extensao import bd


class Exame(bd.Model):
    __tablename__ = 'exames'

    id = bd.Column(bd.Integer, primary_key=True)
    usuario_id = bd.Column(bd.Integer, bd.ForeignKey('usuarios.id'), nullable=False)
    ong_id = bd.Column(bd.Integer, bd.ForeignKey('ong.id'), nullable=False)
    unidade_id = bd.Column(bd.Integer, bd.ForeignKey('unidades.id'), nullable=False)
    data_exame = bd.Column(bd.Date, nullable=False)
    horario = bd.Column(bd.String(5), nullable=False)
    status = bd.Column(bd.String(20), nullable=False, default='agendado')
    criado_em = bd.Column(bd.DateTime, nullable=False, default=datetime.utcnow)

    usuario = bd.relationship('Usuario', back_populates='exames')
    ong = bd.relationship('Ong')
    unidade = bd.relationship('Unidade')

    __table_args__ = (
        bd.UniqueConstraint('usuario_id', 'data_exame', 'horario', name='uq_exame_usuario_horario'),
    )
