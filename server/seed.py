#!/usr/bin/env python3

from random import randint

from faker import Faker

from app import app, db, Customer

fake = Faker()

def make_customers():
    # Delete existing data
    db.session.query(Customer).delete()

    customers = []

    for i in range(3):
        customer = Customer(
            email=fake.email(),
            age=randint(0, 125),
            name=fake.name()
        )
        customers.append(customer)

    db.session.add_all(customers)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        make_customers()