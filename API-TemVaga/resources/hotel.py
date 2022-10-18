from flask_restful import Resource, reqparse

from models.hotel import HotelModel

hoteis = [
    {
        "hotel_id": "alpha",
        "nome": "Alpha Hotel",
        "estrelas": 4.3,
        "diaria": 420.34,
        "cidade":"Rio de Janeiro"
    },
    {
        "hotel_id": "bravo",
        "nome": "Bravo Hotel",
        "estrelas": 4.4,
        "diaria": 380.90,
        "cidade": "Santa Catarina"
    },
    {
        "hotel_id": "charlie",
        "nome": "Charlie Hotel",
        "estrelas": 3.9,
        "diaria": 320.20,
        "cidade": "Santa Catarina"
    }
]

class Hoteis(Resource):
    def get(self):
        return hoteis

class Hotel(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(sefl, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)
        hoteis.append(novo_hotel.json())
        return novo_hotel.json(), 200

    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel_atualizado = novo_hotel.json()
            hotel.update(hotel_atualizado)
            return hotel_atualizado, 200
        hoteis.append(novo_hotel.json())
        return novo_hotel.json(), 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'hotel deleted.'}
