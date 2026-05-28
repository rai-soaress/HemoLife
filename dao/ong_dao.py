from werkzeug.security import generate_password_hash
from extensao import bd
from modelos.ong_modelo import Ong

class OngDAO:

    def buscar_por_email(self, email):
        if not email:
            return None
        return Ong.query.filter_by(email=email.strip().lower()).first()

    def buscar_por_cnpj(self, cnpj):
        if not cnpj:
            return None
        return Ong.query.filter_by(cnpj=cnpj.strip()).first()

    def cadastrar_ong(self, nome, email, senha, cnpj):
        if not nome or not email or not senha or not cnpj:
            return False, 'Preencha todos os campos obrigatórios.'

        if self.buscar_por_email(email):
            return False, 'Já existe uma ONG cadastrada com este email.'

        if self.buscar_por_cnpj(cnpj):
            return False, 'Já existe uma ONG cadastrada com este CNPJ.'

        try:
            ong = Ong(
                nome=nome.strip(),
                email=email.strip().lower(),
                senha=generate_password_hash(senha),
                cnpj=cnpj.strip()
            )
            bd.session.add(ong)
            bd.session.commit()
            return True, 'ONG cadastrada com sucesso.'
        except Exception as e:
            bd.session.rollback()
            print('Erro ao cadastrar ONG:', e)
            return False, 'Erro interno ao cadastrar ONG. Tente novamente.'

    def listar_ongs(self):
        return Ong.query.all()

    def buscar_por_id(self, id):
        return Ong.query.get(int(id))

    def atualizar_ong(self, id, nome, email, cnpj):
        ong = self.buscar_por_id(id)
        if not ong:
            return False, 'ONG não encontrada.'

        if not nome or not email or not cnpj:
            return False, 'Preencha todos os campos obrigatórios.'

        email_existente = Ong.query.filter(Ong.id != id, Ong.email == email.strip().lower()).first()
        if email_existente:
            return False, 'Outro cadastro de ONG já utiliza este email.'

        cnpj_existente = Ong.query.filter(Ong.id != id, Ong.cnpj == cnpj.strip()).first()
        if cnpj_existente:
            return False, 'Outro cadastro de ONG já utiliza este CNPJ.'

        ong.nome = nome.strip()
        ong.email = email.strip().lower()
        ong.cnpj = cnpj.strip()

        try:
            bd.session.commit()
            return True, 'ONG atualizada com sucesso.'
        except Exception as e:
            bd.session.rollback()
            print('Erro ao atualizar ONG:', e)
            return False, 'Erro interno ao atualizar ONG. Tente novamente.'

    def deletar_ong(self, id):
        ong = self.buscar_por_id(id)
        if ong:
            bd.session.delete(ong)
            bd.session.commit()
            return True
        return False