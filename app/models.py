from datetime import datetime
from app import db
from app import login
from flask_login import UserMixin
import json
from json import JSONEncoder



"""Users Class - Database"""

class Users(UserMixin, db.Model):
   __tablename__ = 'Users'
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(50), unique=True, nullable=False)
   email = db.Column(db.String(100), nullable=False)
   password = db.Column(db.String(150), nullable=False)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   modified_at = db.Column(db.DateTime, default=datetime.utcnow)
   
   def __repr__(self):
        return self.username


"""Vehicles Class - Database"""

class Vehicles(db.Model):
      __tablename__ = 'Vehicles'
      vehicle_id = db.Column(db.String(255), unique=True, primary_key=True)
      vehicle_type = db.Column(db.String(50) ,  nullable=False)
      count_vechicle = db.Column(db.Integer, nullable=False)
      
      def __repr__(self):
            value = {"vehicle_id":self.vehicle_id , "vehcile_type":self.vehicle_type ,"count_vehicle": self.count_vechicle}
            return str(value)

"""Customers Class - Database"""

class Customers(db.Model):
   __tablename__ = 'Customers'
   cust_id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
   cust_name = db.Column(db.String(50), nullable=False)
   cust_ph_no = db.Column(db.String(100), nullable=False)
   cust_email = db.Column(db.String(150), nullable=False)
   cust_added_at = db.Column(db.DateTime, default=datetime.utcnow)
   
   def __repr__(self):
        return '<Customers {}>'.format(self.cust_id)

"""Rentals Class - Database"""

class Rentals(db.Model):
   __tablename__ = 'Rentals'
   rent_id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
   cust_id = db.Column(db.Integer, db.ForeignKey('Customers.cust_id'))
   cust_name = db.Column(db.String(50), nullable=False)
   veh_type = db.Column(db.String(100), nullable=False)
   rental_date = db.Column(db.DateTime, nullable=False)
   return_date = db.Column(db.DateTime , nullable = False)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   
   def __repr__(self):
        return '<Rentals {}>'.format(self.rent_id)


class Encoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

@login.user_loader
def load_user(id):
       return Users.query.get(int(id)) 