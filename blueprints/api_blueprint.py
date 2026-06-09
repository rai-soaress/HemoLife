from flask import Blueprint, jsonify

from dao.ong_dao import OngDAO
from dao.unidade_dao import UnidadeDAO

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/unidades', methods=['GET'])
def listar_unidades():
    unidades = UnidadeDAO().listar_unidades()

    resultado = []
    for unidade in unidades:
        resultado.append({
            'id': unidade.id,
            'nome': unidade.nome,
            'telefone': unidade.telefone,
            'endereco': unidade.endereco,
        })

    return jsonify(resultado)


@api_bp.route('/ongs', methods=['GET'])
def listar_ongs():
    ongs = OngDAO().listar_ongs()

    resultado = []
    for ong in ongs:
        resultado.append({
            'id': ong.id,
            'nome': ong.nome,
            'email': ong.email,
            'cnpj': ong.cnpj,
        })

    return jsonify(resultado)
