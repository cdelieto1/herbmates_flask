"""Automate the db creation and population"""

import os, json, crud, model, server
from datetime import datetime
from model import *


os.system('dropdb herbmates')
os.system('createdb herbmates')

model.connect_to_db(server.app)
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