from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from models.models import Mercadoria, Entrada, Saida, db

routes = Blueprint('routes', __name__)

@routes.route('/api/mercadorias', methods=['GET'])
def get_mercadorias():
    mercadorias = Mercadoria.query.all()
    mercadorias_list = []

    for mercadoria in mercadorias:
        mercadoria_data = {
            'id': mercadoria.id,
            'nome': mercadoria.nome,
            'registro': mercadoria.registro,
            'fabricante': mercadoria.fabricante,
            'tipo': mercadoria.tipo,
            'descricao': mercadoria.descricao
        }
        mercadorias_list.append(mercadoria_data)

    return jsonify(mercadorias_list)

@routes.route('/api/cadastrar_mercadoria', methods=['POST'])
def cadastrar_mercadoria():
    data = request.json

    existing_mercadoria = Mercadoria.query.filter_by(nome=data['nome']).first()
    if existing_mercadoria:
        return jsonify({'error': 'Mercadoria já cadastrada'}), 400

    nova_mercadoria = Mercadoria(
        nome=data['nome'],
        registro=data['registro'],
        fabricante=data['fabricante'],
        tipo=data['tipo'],
        descricao=data['descricao']
    )

    db.session.add(nova_mercadoria)
    db.session.commit()

    return jsonify({'message': 'Mercadoria cadastrada com sucesso!'})

@routes.route('/api/entrada', methods=['POST'])
def cadastrar_entrada():
    data = request.json
    mercadoria_id = data['mercadoria_id']

    try:
        mercadoria = Mercadoria.query.filter_by(id=mercadoria_id).one()
    except NoResultFound:
        return jsonify({'error': 'Mercadoria não encontrada'}), 404

    entrada = Entrada(
        quantidade=data['quantidade'],
        data_hora=datetime.now(),
        local=data['local'],
        mercadoria_id=mercadoria_id
    )

    db.session.add(entrada)
    db.session.commit()
    return jsonify({'message': 'Entrada cadastrada com sucesso!'})

@routes.route('/api/saida', methods=['POST'])
def cadastrar_saida():
    data = request.json
    saida = Saida(
        quantidade=data['quantidade'],
        data_hora=data['data_hora'],
        local=data['local'],
        mercadoria_id=data['mercadoria_id']
    )
    db.session.add(saida)
    db.session.commit()
    return jsonify({'message': 'Saída cadastrada com sucesso!'})