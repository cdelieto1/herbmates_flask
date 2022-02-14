"""Automate the db creation and population"""

import os, json, crud, model, server
from datetime import datetime
from model import *
from server import app

def example_data(is_testing=True):

    if is_testing:
        os.system('dropdb herbmatestest')
        os.system('createdb herbmatestest')
        model.connect_to_db(app, "postgresql:///herbmatestest")
    else:
        os.system('dropdb d9duoauc48c6p0')
        os.system('createdb d9duoauc48c6p0')
        #model.connect_to_db(server.app)
        model.connect_to_db(app, db_url)

    model.db.create_all()


    # create complexes
    complex1 = Complex(complex_name='Montague', complex_address='1234 Mission st')
    complex2 = Complex(complex_name='l 7', complex_address='1222 Harrison st')
    db.session.add(complex1)
    db.session.add(complex2)
    db.session.commit()


    # create descriptions
    descript1 = Description(herb_name='Oregano', descript='Oregano', img_url='/oregano.jpg')
    descript2 = Description(herb_name='Parsley', descript='Parsley', img_url='/parsley.jpg')
    descript3 = Description(herb_name='Thyme', descript='Thyme', img_url='/thyme.jpg')
    descript4 = Description(herb_name='Basil', descript='Basil', img_url='/basil.jpg')
    descript5 = Description(herb_name='Rosemary', descript='Rosemary', img_url='/rosemary.jpg')
    descript6 = Description(herb_name='Cilantro', descript='Cilantro', img_url='/cilantro.jpg')
    db.session.add(descript1)
    db.session.add(descript2)
    db.session.add(descript3)
    db.session.add(descript4)
    db.session.add(descript5)
    db.session.add(descript6)
    db.session.commit()

    # create dummy user 
    user1 = User(email='cassie1@gmail.com', password='hello', fname='Cassie', lname='Delieto', mobile_number='+19513759375', complex_id=1)
    db.session.add(user1)
    db.session.commit()
    user2 = User(email='cassie2@gmail.com', password='hello', fname='Jennifer', lname='Dorito', mobile_number='+14154843593', complex_id=1)
    db.session.add(user2)
    db.session.commit()
     
    status0 = Status(status_id=0, status='inactive')
    status1 = Status(status_id=1, status='active')
    status2 = Status(status_id=2, status='requested')
    status3 = Status(status_id=3, status='ready')
    status4 = Status(status_id=4, status='completed')
    db.session.add(status0)
    db.session.add(status1)
    db.session.add(status2)
    db.session.add(status3)
    db.session.add(status4)
    db.session.commit()

if __name__ == '__main__':
    example_data(False) #populates production database if you just run seed_database.py like a normal script
