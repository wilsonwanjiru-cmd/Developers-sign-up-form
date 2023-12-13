from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
ma = Marshmallow(app)

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'age': self.age}

@app.route("/customers", methods=['GET', 'POST', 'DELETE'])
def customers():
    if request.method == 'GET':
        customers_list = [customer.to_dict() for customer in Customer.query.all()]
        return make_response(jsonify(customers_list))

    if request.method == 'POST':
        data = request.get_json()
        new_customer = Customer(name=data.get('name'), email=data.get('email'), age=data.get('age'))
        db.session.add(new_customer)
        db.session.commit()
        return make_response(jsonify(new_customer.to_dict()))

    if request.method == 'DELETE':
        customer_id = request.args.get('id')
        if customer_id:
            customer = Customer.query.get(customer_id)
            if customer:
                db.session.delete(customer)
                db.session.commit()
                return make_response(jsonify({'message': 'Customer deleted successfully'}), 200)
            else:
                return make_response(jsonify({'message': 'Customer not found'}), 404)
        else:
            return make_response(jsonify({'message': 'Customer ID is required for deletion'}), 400)

if __name__ == "__main__":
    app.run(port="5555")
