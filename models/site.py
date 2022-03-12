from sql_alchemy import database

class SiteModel(database.Model):
    __tablename__ = 'sites'
    
    id = database.Column(database.Integer, primary_key = True)
    url = database.Column(database.String(40))
    hoteis = database.relationship('HotelModel')

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            "id": self.id,
            "url": self.url,
            "hoteis": [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find(cls, url):
        site = cls.query.filter_by(url = url).first()
        if site:
            return site
        return None

    @classmethod
    def find_by_id(cls, site_id):
        site = cls.query.filter_by(id = site_id).first()
        if site:
            return site
        return None

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):

        # deletando todos os hoteis que contem este site utilizando list compreensions
        [hotel.delete() for hotel in self.hoteis]

        database.session.delete(self)
        database.session.commit()