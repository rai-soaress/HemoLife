from extensao import bd
from modelos.usuario_modelo import Usuario
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash


class UsuarioDAO:

    def criar(self, nome, email, senha, tipo, perfil):
        try:
            nome = self._normalizar_texto(nome)
            email = self._normalizar_email(email)
            senha = self._normalizar_texto(senha)
            tipo = self._normalizar_texto(tipo)
            perfil = self._normalizar_texto(perfil)

            if not nome or not email or not senha:
                return False, "Preencha todos os campos obrigatorios."

            if perfil not in ('admin', 'doador'):
                return False, "Perfil invalido."

            if Usuario.query.filter_by(email=email).first():
                return False, "Ja existe um usuario cadastrado com este email."

            if perfil == 'admin':
                tipo_final = None
            elif perfil == 'doador':
                if not tipo:
                    return False, "Informe o tipo sanguineo."
                tipo_final = tipo

            usuario = Usuario(
                nome=nome,
                email=email,
                senha=generate_password_hash(senha),
                tipo_sanguineo=tipo_final,
                perfil=perfil
            )

            bd.session.add(usuario)
            bd.session.commit()
            return True, "Cadastro realizado com sucesso."
        except IntegrityError as erro:
            bd.session.rollback()
            print(f"Erro de integridade ao criar usuario: {erro}")
            return False, "Email ja cadastrado."
        except SQLAlchemyError as erro:
            bd.session.rollback()
            print(f"Erro ao criar usuario: {erro}")
            return False, "Erro ao cadastrar usuario. Tente novamente."

    def validar_login(self, email, senha):
        email = self._normalizar_email(email)
        senha = self._normalizar_texto(senha)

        if not email or not senha:
            return None

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            return None

        if self._senha_hash_valida(usuario.senha, senha):
            return usuario

        if usuario.senha == senha:
            usuario.senha = generate_password_hash(senha)
            bd.session.commit()
            return usuario

        return None

    def buscar_por_id(self, id):
        try:
            return bd.session.get(Usuario, int(id))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _normalizar_texto(valor):
        return valor.strip() if isinstance(valor, str) else valor

    @staticmethod
    def _normalizar_email(valor):
        return valor.strip().lower() if isinstance(valor, str) else valor

    @staticmethod
    def _senha_hash_valida(senha_salva, senha_digitada):
        try:
            return check_password_hash(senha_salva, senha_digitada)
        except (TypeError, ValueError):
            return False
