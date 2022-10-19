from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {"hoteis": [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    atributos.add_argument('diaria', type=float)
    atributos.add_argument('cidade', type=str)

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
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return hotel.json(), 200


    def put(self, hotel_id):
        data = Hotel.atributos.parse_args()

        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            hotel_found.update_hotel(**data)
            try:
                hotel_found.save_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel."}, 500
            return hotel_found.json(), 200

        new_hotel = HotelModel(hotel_id, **data)
        try:
            new_hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return new_hotel.json(), 201

    def delete(self, hotel_id):
        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            try:
                hotel_found.delete_hotel()
            except:
                return {"message": "An internal error ocurred trying to delete hotel."}, 500
            return {"message": "Hotel deleted."}
        return {"message": "Hotel not found."}, 404
