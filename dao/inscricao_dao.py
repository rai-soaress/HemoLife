from extensao import bd
from modelos.inscricao_modelo import Inscricao
from modelos.ong_modelo import Ong
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class InscricaoDAO:

    def inscrever(self, usuario_id, ong_id):
        try:
            if not bd.session.get(Ong, int(ong_id)):
                return False, "ONG nao encontrada."

            existe = Inscricao.query.filter_by(
                usuario_id=usuario_id,
                ong_id=ong_id
            ).first()

            if existe:
                return False, "Voce ja esta inscrito nesta ONG."

            insc = Inscricao(usuario_id=usuario_id, ong_id=ong_id)
            bd.session.add(insc)
            bd.session.commit()
            return True, "Inscricao realizada com sucesso."

        except (TypeError, ValueError):
            bd.session.rollback()
            return False, "ONG invalida."
        except IntegrityError as erro:
            bd.session.rollback()
            print(f"Erro de integridade ao inscrever em ONG: {erro}")
            return False, "Voce ja esta inscrito nesta ONG."
        except SQLAlchemyError as erro:
            bd.session.rollback()
            print(f"Erro ao inscrever em ONG: {erro}")
            return False, "Erro ao realizar inscricao. Tente novamente."


    def cancelar(self, usuario_id, ong_id):
        try:
            insc = Inscricao.query.filter_by(
                usuario_id=usuario_id,
                ong_id=ong_id
            ).first()

            if not insc:
                return False, "Inscricao nao encontrada."

            bd.session.delete(insc)
            bd.session.commit()
            return True, "Inscricao cancelada com sucesso."
        except SQLAlchemyError as erro:
            bd.session.rollback()
            print(f"Erro ao cancelar inscricao: {erro}")
            return False, "Erro ao cancelar inscricao. Tente novamente."


    def listar_ongs_do_usuario(self, usuario_id):
        insc = Inscricao.query.filter_by(usuario_id=usuario_id).all()
        return [i.ong for i in insc]


    def ja_inscrito(self, usuario_id, ong_id):
        return Inscricao.query.filter_by(
            usuario_id=usuario_id,
            ong_id=ong_id
        ).first() is not None
