from sql_alchemy import database

class UserModel(database.Model):
    __tablename__ = 'users'
    
    id = database.Column(database.Integer, primary_key = True)
    email = database.Column(database.String(40))
    password = database.Column(database.String(40))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "email": self.email
        }

    @classmethod
    def find(cls, id):
        user = cls.query.filter_by(id = id).first()
        if user:
            return user
        return None

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email = email).first()
        if user:
            return user
        return None