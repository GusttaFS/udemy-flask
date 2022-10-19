from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {"hoteis": [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found."}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400

        data = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **data)
        hotel.save_hotel()
        return hotel.json(), 200


    def put(self, hotel_id):
        data = Hotel.atributos.parse_args()

        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            hotel_found.update_hotel(**data)
            hotel_found.save_hotel()
            return hotel_found.json(), 200

        new_hotel = HotelModel(hotel_id, **data)
        new_hotel.save_hotel()
        return new_hotel.json(), 201

    def delete(self, hotel_id):
        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            hotel_found.delete_hotel()
            return {"message": "Hotel deleted."}
        return {"message": "Hotel not found."}, 404
