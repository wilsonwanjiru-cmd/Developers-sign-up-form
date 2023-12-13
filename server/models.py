from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'age': self.age}

    def __repr__(self):
        return f'Customer: {self.name}, age: {self.age}, email: {self.email}'