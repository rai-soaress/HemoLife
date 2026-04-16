from extensao import bd
from modelos.usuario_modelo import Usuario

class UsuarioDAO:
    
    def criar(self, nome, email, senha, tipo, perfil):
        try:
            tipo_final = None if perfil == 'admin' else tipo
            
            novo_usuario = Usuario(
                nome=nome, 
                email=email, 
                senha=senha, 
                tipo_sanguineo=tipo_final, 
                perfil=perfil
            )
            
            bd.session.add(novo_usuario)
            bd.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar: {e}")
            bd.session.rollback()
            return False

    def validar_login(self, email, senha):
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha == senha:
            return usuario
        return None

    def buscar_por_id(self, id_usuario):
        return Usuario.query.get(int(id_usuario))


    def listar_todos(self):
        return Usuario.query.all()

    def excluir(self, id_usuario):
        try:
            usuario = Usuario.query.get(id_usuario)
            if usuario:
                bd.session.delete(usuario)
                bd.session.commit()
                return True
            return False
        except:
            bd.session.rollback()
            return False