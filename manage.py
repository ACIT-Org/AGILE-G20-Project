from sqlalchemy import select
from models import Product, Customer, Order, ProductOrder
from db import db
from app import app
import sys
import csv
import random
from datetime import datetime as dt
from datetime import timedelta

# This file was used to read data from a CSV which we can use to put a bunch of data into our database after we create our tables
# IGNORE THIS FILE FOR NOW

def csv_reader(filename):
    customer_list=[]

    if filename == "products.csv":
        with open(filename, "r") as file:
            content= csv.DictReader(file)

            for product in content:
                possible_category = db.session.execute(select(Category).where(Category.name == product["category"])).scalar()
                if not possible_category:
                    category_obj = Category(name=product["category"])
                    db.session.add(category_obj)
                else:
                    category_obj = possible_category
                    product = Product(name=product["name"], price=float(product["price"]), available=product["available"], category=category_obj)
                    db.session.add(product)

    elif filename == "customers.csv":
        with open(filename, "r") as file:
            content= csv.DictReader(file)
            for line in content:
                customer_list.append(Customer(name=line["name"], phone=line['phone']))

        for customer in customer_list:
            db.session.add(customer)
    db.session.commit() 

def generate():
    random_customer = db.session.execute(select(Customer).order_by(db.func.random())).scalar()
    num_prods = random.randint(4, 6) 
    random_prods = db.session.execute(select(Product).order_by(db.func.random()).limit(num_prods)).scalars()

    random_time = dt.now().replace(microsecond=0) - timedelta(days=random.randint(1, 3), hours=random.randint(0, 15), minutes=random.randint(0, 30))
    my_order = Order(customer=random_customer, created=random_time)

    for element in random_prods: 
        print(element)
        found_product = ProductOrder(product=element, quantity=random.randint(1, 5), order = my_order)
        db.session.add(found_product)

    my_order.amount = my_order.calculate_total()
    


if __name__ == "__main__":
     with app.app_context():
        db.drop_all()
        db.create_all()
        
        # csv_reader("products.csv")
        # csv_reader("customers.csv")

        # for i in range(20):
        #     generate() #20 orders get generated here

        db.session.commit()


