from flask import Blueprint, request, jsonify
from pokecard_inventory.helpers import token_required
from pokecard_inventory.models import db, Poke_Card, poke_schema, pokes_schema

api = Blueprint('api', __name__, url_prefix='/api')

# @api.route('/getdata')
# def getdata():
#     return {'some': 'value'}

@api.route('/pokecards', methods = ['POST'])
@token_required
def create_card(our_user):

    name = request.json['name']
    type = request.json['type']
    series = request.json['series']
    year = request.json['year']
    collector_card_number = request.json['collector_card_number']
    is_graded = request.json['is_graded']
    grade = request.json['grade']
    description = request.json['description']
    for_sale = request.json['for_sale']
    user_token = our_user.token

    print(f'User Token: {our_user.token}')

    card = Poke_Card(name, type, series, year, collector_card_number, is_graded, grade, description, for_sale, user_token)

    db.session.add(card)
    db.session.commit()

    response = poke_schema.dump(card)

    return jsonify(response)

@api.route('/pokecards/<id>', methods = ['GET'])
@token_required
def one_card(our_user, id):
    if id:
        card = Poke_Card.query.get(id)
        response = poke_schema.dump(card)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

@api.route('/pokecards', methods = ['GET'])
@token_required
def all_cards(our_user):
    token = our_user.token
    cards = Poke_Card.query.filter_by(user_token = token).all()
    response = pokes_schema.dump(cards)

    return jsonify(response)


@api.route('/pokecards/<id>', methods = {'PUT'})
@token_required
def update_card(our_user, id):
    card = Poke_Card.query.get(id)

    card.name = request.json['name']
    card.type = request.json['type']
    card.series = request.json['series']
    card.year = request.json['year']
    card.collector_card_number = request.json['collector_card_number']
    card.is_graded = request.json['is_graded']
    card.grade = request.json['grade']
    card.description = request.json['description']
    card.for_sale = request.json['for_sale']
    card.user_token = our_user.token

    db.session.commit()

    response = poke_schema.dump(card)

    return jsonify(response)

@api.route('/pokecards/<id>', methods = ['DELETE'])
@token_required
def delete_card(our_user, id):
    card = Poke_Card.query.get(id)
    db.session.delete(card)
    db.session.commit()

    response = poke_schema.dump(card)

    return jsonify(response)