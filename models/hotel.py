from sql_alchemy import database

class HotelModel(database.Model):
    __tablename__ = 'hoteis'
    
    id = database.Column(database.Integer, primary_key = True)
    site_id = database.Column(database.Integer, database.ForeignKey('sites.id'))
    name = database.Column(database.String(40))
    stars = database.Column(database.Float(precision=1))
    price = database.Column(database.Float(precision=2))
    city = database.Column(database.String(40))
    
    def __init__(self, id, site_id, name, stars, price, city):
        self.id = id
        self.site_id = site_id
        self.name = name
        self.stars = stars
        self.price = price
        self.city = city

    def json(self):
        return {
            "id": self.id,
            "site_id": self.site_id,
            "name": self.name,
            "stars": self.stars,
            "price": self.price,
            "city": self.city
        }

    @classmethod
    def find(cls, id):
        hotel = cls.query.filter_by(id = id).first()
        if hotel:
            return hotel
        return None

    def save(self):
        database.session.add(self)
        database.session.commit()

    def update(self, name, stars, price, city):
        self.name = name
        self.stars = stars
        self.price = price
        self.city = city

    def delete(self):
        database.session.delete(self)
        database.session.commit()