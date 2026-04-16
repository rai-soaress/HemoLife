from extensao import bd
from modelos.usuario_modelo import Usuario

class UsuarioDAO:

    def criar(self, nome, email, senha, tipo, perfil):
        try:
            tipo_final = None if perfil == 'admin' else tipo

            usuario = Usuario(
                nome=nome,
                email=email,
                senha=senha,
                tipo_sanguineo=tipo_final,
                perfil=perfil
            )

            bd.session.add(usuario)
            bd.session.commit()
            return True
        except:
            bd.session.rollback()
            return False

    def validar_login(self, email, senha):
        return Usuario.query.filter_by(email=email, senha=senha).first()

    def buscar_por_id(self, id):
        return Usuario.query.get(int(id))