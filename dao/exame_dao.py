from datetime import date, datetime

from extensao import bd
from modelos.exame_modelo import Exame
from modelos.inscricao_modelo import Inscricao
from modelos.ong_modelo import Ong
from modelos.unidade_modelo import Unidade
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class ExameDAO:

    def agendar(self, usuario_id, ong_id, unidade_id, data_exame, horario):
        try:
            ong_id = int(ong_id)
            unidade_id = int(unidade_id)
            data_final = self._parse_data(data_exame)
            horario_final = self._normalizar_horario(horario)

            if not ong_id or not unidade_id or not data_final or not horario_final:
                return False, "Preencha ONG, unidade, data e horario."

            if data_final < date.today():
                return False, "Escolha uma data futura para o exame."

            if not bd.session.get(Ong, ong_id):
                return False, "ONG nao encontrada."

            inscrito = Inscricao.query.filter_by(
                usuario_id=usuario_id,
                ong_id=ong_id,
            ).first()
            if not inscrito:
                return False, "Voce so pode marcar exames por ONGs em que esta inscrito."

            if not bd.session.get(Unidade, unidade_id):
                return False, "Unidade nao encontrada."

            exame = Exame(
                usuario_id=usuario_id,
                ong_id=ong_id,
                unidade_id=unidade_id,
                data_exame=data_final,
                horario=horario_final,
            )
            bd.session.add(exame)
            bd.session.commit()
            return True, "Exame agendado com sucesso."
        except (TypeError, ValueError):
            bd.session.rollback()
            return False, "Dados de agendamento invalidos."
        except IntegrityError:
            bd.session.rollback()
            return False, "Voce ja tem um exame neste dia e horario."
        except SQLAlchemyError as erro:
            bd.session.rollback()
            print(f"Erro ao agendar exame: {erro}")
            return False, "Erro ao agendar exame. Tente novamente."

    def listar_do_usuario(self, usuario_id):
        return (
            Exame.query
            .filter_by(usuario_id=usuario_id)
            .order_by(Exame.data_exame.asc(), Exame.horario.asc())
            .all()
        )

    def cancelar(self, usuario_id, exame_id):
        try:
            exame = Exame.query.filter_by(id=exame_id, usuario_id=usuario_id).first()
            if not exame:
                return False, "Exame nao encontrado."

            exame.status = 'cancelado'
            bd.session.commit()
            return True, "Exame cancelado com sucesso."
        except SQLAlchemyError as erro:
            bd.session.rollback()
            print(f"Erro ao cancelar exame: {erro}")
            return False, "Erro ao cancelar exame. Tente novamente."

    @staticmethod
    def _parse_data(valor):
        if isinstance(valor, date):
            return valor
        if not isinstance(valor, str):
            return None
        return datetime.strptime(valor.strip(), '%Y-%m-%d').date()

    @staticmethod
    def _normalizar_horario(valor):
        if not isinstance(valor, str):
            return None
        valor = valor.strip()
        try:
            datetime.strptime(valor, '%H:%M')
        except ValueError:
            return None
        return valor
