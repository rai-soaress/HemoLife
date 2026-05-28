from extensao import bd
from modelos.ong_modelo import Ong
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash


class OngDAO:

    def cadastrar_ong(self, nome, email, senha, cnpj):
        try:
            nome = self._normalizar_texto(nome)
            email = self._normalizar_email(email)
            senha = self._normalizar_texto(senha)
            cnpj = self._normalizar_texto(cnpj)

            if not nome or not email or not senha or not cnpj:
                return False, "Preencha todos os campos obrigatorios."

            if Ong.query.filter_by(email=email).first():
                return False, "Ja existe uma ONG cadastrada com este email."

            if Ong.query.filter_by(cnpj=cnpj).first():
                return False, "Ja existe uma ONG cadastrada com este CNPJ."

            ong = Ong(nome=nome, email=email, senha=generate_password_hash(senha), cnpj=cnpj)
            bd.session.add(ong)
            bd.session.commit()
            return True, "ONG cadastrada com sucesso."
        except IntegrityError as erro:
            bd.session.rollback()
            print(f"Erro de integridade ao cadastrar ONG: {erro}")
            return False, "Email ou CNPJ ja cadastrado."
        except SQLAlchemyError as erro:
            bd.session.rollback()
            print(f"Erro ao cadastrar ONG: {erro}")
            return False, "Erro ao cadastrar ONG. Tente novamente."

    def listar_ongs(self):
        return Ong.query.order_by(Ong.nome.asc()).all()

    def verificar_login(self, email, senha):
        email = self._normalizar_email(email)
        senha = self._normalizar_texto(senha)

        if not email or not senha:
            return None

        ong = Ong.query.filter_by(email=email).first()
        if not ong:
            return None

        try:
            if check_password_hash(ong.senha, senha):
                return ong
        except (TypeError, ValueError):
            pass

        if ong.senha == senha:
            ong.senha = generate_password_hash(senha)
            bd.session.commit()
            return ong

        return None

    def buscar_por_id(self, id):
        try:
            return bd.session.get(Ong, int(id))
        except (TypeError, ValueError):
            return None

    def atualizar_ong(self, id, nome, email, cnpj):
        try:
            nome = self._normalizar_texto(nome)
            email = self._normalizar_email(email)
            cnpj = self._normalizar_texto(cnpj)

            if not nome or not email or not cnpj:
                return False, "Preencha todos os campos obrigatorios."

            ong = self.buscar_por_id(id)
            if not ong:
                return False, "ONG nao encontrada."

            email_usado = Ong.query.filter(Ong.email == email, Ong.id != ong.id).first()
            if email_usado:
                return False, "Ja existe outra ONG com este email."

            cnpj_usado = Ong.query.filter(Ong.cnpj == cnpj, Ong.id != ong.id).first()
            if cnpj_usado:
                return False, "Ja existe outra ONG com este CNPJ."

            ong.nome = nome
            ong.email = email
            ong.cnpj = cnpj
            bd.session.commit()
            return True, "ONG atualizada com sucesso."
        except IntegrityError as erro:
            bd.session.rollback()
            print(f"Erro de integridade ao atualizar ONG: {erro}")
            return False, "Email ou CNPJ ja cadastrado."
        except SQLAlchemyError as erro:
            bd.session.rollback()
            print(f"Erro ao atualizar ONG: {erro}")
            return False, "Erro ao atualizar ONG. Tente novamente."

    def deletar_ong(self, id):
        try:
            ong = self.buscar_por_id(id)
            if not ong:
                return False

            bd.session.delete(ong)
            bd.session.commit()
            return True
        except SQLAlchemyError:
            bd.session.rollback()
            return False

    @staticmethod
    def _normalizar_texto(valor):
        return valor.strip() if isinstance(valor, str) else valor

    @staticmethod
    def _normalizar_email(valor):
        return valor.strip().lower() if isinstance(valor, str) else valor
