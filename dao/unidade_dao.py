from extensao import bd
from modelos.unidade_modelo import Unidade
from sqlalchemy.exc import SQLAlchemyError


class UnidadeDAO:

    def listar_unidades(self):
        return Unidade.query.order_by(Unidade.nome.asc()).all()

    def criar(self, nome, telefone, endereco):
        try:
            nome = self._normalizar_texto(nome)
            telefone = self._normalizar_texto(telefone)
            endereco = self._normalizar_texto(endereco)

            if not nome or not telefone or not endereco:
                return False

            unidade = Unidade(nome=nome, telefone=telefone, endereco=endereco)
            bd.session.add(unidade)
            bd.session.commit()
            return True
        except SQLAlchemyError:
            bd.session.rollback()
            return False

    @staticmethod
    def _normalizar_texto(valor):
        return valor.strip() if isinstance(valor, str) else valor
