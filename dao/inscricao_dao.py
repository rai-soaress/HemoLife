from extensao import bd
from modelos.inscricao_modelo import Inscricao

class InscricaoDAO:

    def inscrever(self, usuario_id, ong_id):
        try:
            existe = Inscricao.query.filter_by(
                usuario_id=usuario_id,
                ong_id=ong_id
            ).first()

            if existe:
                return False

            insc = Inscricao(usuario_id=usuario_id, ong_id=ong_id)
            bd.session.add(insc)
            bd.session.commit()
            return True

        except Exception as e:
            print("ERRO:", e)
            bd.session.rollback()
            return False


    def cancelar(self, usuario_id, ong_id):
        insc = Inscricao.query.filter_by(
            usuario_id=usuario_id,
            ong_id=ong_id
        ).first()

        if insc:
            bd.session.delete(insc)
            bd.session.commit()


    def listar_ongs_do_usuario(self, usuario_id):
        insc = Inscricao.query.filter_by(usuario_id=usuario_id).all()
        return [i.ong for i in insc]


    def ja_inscrito(self, usuario_id, ong_id):
        return Inscricao.query.filter_by(
            usuario_id=usuario_id,
            ong_id=ong_id
        ).first() is not None