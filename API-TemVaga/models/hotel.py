from sql_alchemy import db

class HotelModel(db.Model):
    
    __tablename__ = 'hoteis'

    hotel_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(80))
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(40))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }
        