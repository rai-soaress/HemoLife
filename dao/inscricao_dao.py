from extensao import bd
from modelos.inscricao_modelo import Inscricao

class InscricaoDAO:

    def inscrever(self, usuario_id, ong_id):
        if not usuario_id or not ong_id:
            return False, 'Dados inválidos para inscrição.'

        existe = Inscricao.query.filter_by(
            usuario_id=usuario_id,
            ong_id=ong_id
        ).first()

        if existe:
            return False, 'Você já está inscrito nesta ONG.'

        try:
            insc = Inscricao(usuario_id=usuario_id, ong_id=ong_id)
            bd.session.add(insc)
            bd.session.commit()
            return True, 'Inscrição realizada com sucesso.'
        except Exception as e:
            print('Erro ao inscrever:', e)
            bd.session.rollback()
            return False, 'Erro interno ao inscrever. Tente novamente.'

    def cancelar(self, usuario_id, ong_id):
        insc = Inscricao.query.filter_by(
            usuario_id=usuario_id,
            ong_id=ong_id
        ).first()

        if insc:
            bd.session.delete(insc)
            bd.session.commit()
            return True, 'Inscrição cancelada com sucesso.'

        return False, 'Inscrição não encontrada.'

    def listar_ongs_do_usuario(self, usuario_id):
        insc = Inscricao.query.filter_by(usuario_id=usuario_id).all()
        return [i.ong for i in insc]

    def ja_inscrito(self, usuario_id, ong_id):
        return Inscricao.query.filter_by(
            usuario_id=usuario_id,
            ong_id=ong_id
        ).first() is not None