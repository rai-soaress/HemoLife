from flask import Blueprint, jsonify

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
