from sqlalchemy import select , create_engine , update
from flask import session
import json
from app import db
from app.models import Users,Vehicles , Encoder , Customers , Rentals
import datetime
import json

"""class to encode json data to make serializable"""

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)


"""function to update inventory"""

engine = create_engine('mysql://rentals:bookings@localhost/rentals')
def inventory_update(type):

    conn = engine.connect()
    pk = select(Vehicles.vehicle_id).where(Vehicles.vehicle_type ==type)

    for j in conn.execute(pk):
        id = j.vehicle_id
    X = Vehicles.query.get(id)
    X.count_vechicle = X.count_vechicle-1

    if X.count_vechicle >= 0:
        db.session.commit()
    else:
      print("Not Right Choice")

    return None

"""function to check vehcile available details from database"""

def check_inventory(type):

    conn = engine.connect()
    check = select(Vehicles.count_vechicle).where(Vehicles.vehicle_type ==type)

    for i in conn.execute(check):
        count = i.count_vechicle

    if count >= 1: 
         return None
    else:
         return f'Vehicle "{type}" cannot be rented as it is already booked!! Goto Home for View and to Check Inventory Data!'
     
