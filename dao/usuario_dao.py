from werkzeug.security import generate_password_hash, check_password_hash
from extensao import bd
from modelos.usuario_modelo import Usuario

class UsuarioDAO:

    def buscar_por_email(self, email):
        if not email:
            return None
        return Usuario.query.filter_by(email=email.strip().lower()).first()

    def criar(self, nome, email, senha, tipo, perfil):
        if not nome or not email or not senha or not perfil:
            return False, 'Preencha todos os campos obrigatórios.'

        if perfil not in ('admin', 'doador', 'receptor'):
            return False, 'Perfil inválido. Escolha admin ou doador.'

        if self.buscar_por_email(email):
            return False, 'Já existe um usuário cadastrado com este email.'

        tipo_final = None if perfil == 'admin' else tipo

        usuario = Usuario(
            nome=nome.strip(),
            email=email.strip().lower(),
            senha=generate_password_hash(senha),
            tipo_sanguineo=tipo_final.strip() if tipo_final else None,
            perfil='doador' if perfil == 'receptor' else perfil
        )

        try:
            bd.session.add(usuario)
            bd.session.commit()
            return True, 'Cadastro realizado com sucesso. Faça login para continuar.'
        except Exception as e:
            bd.session.rollback()
            print('Erro ao criar usuário:', e)
            return False, 'Erro interno ao cadastrar usuário. Tente novamente.'

    def validar_login(self, email, senha):
        usuario = self.buscar_por_email(email)
        if not usuario:
            return None

        if check_password_hash(usuario.senha, senha):
            return usuario

        # Compatibilidade com senhas antigas armazenadas em texto puro
        if usuario.senha == senha:
            return usuario

        return None

    def buscar_por_id(self, id):
        return Usuario.query.get(int(id))