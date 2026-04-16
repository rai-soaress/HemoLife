from extensao import bd
from modelos.ong_modelo import Ong

class OngDAO:

    def cadastrar_ong(self, nome, email, senha, cnpj):
        try:
            ong = Ong(nome=nome, email=email, senha=senha, cnpj=cnpj)
            bd.session.add(ong)
            bd.session.commit()
            return True
        except:
            bd.session.rollback()
            return False

    def listar_ongs(self):
        return Ong.query.all()

    def buscar_por_id(self, id):
        return Ong.query.get(id)

    def atualizar_ong(self, id, nome, email, cnpj):
        ong = self.buscar_por_id(id)
        if ong:
            ong.nome = nome
            ong.email = email
            ong.cnpj = cnpj
            bd.session.commit()

    def deletar_ong(self, id):
        ong = self.buscar_por_id(id)
        if ong:
            bd.session.delete(ong)
            bd.session.commit()