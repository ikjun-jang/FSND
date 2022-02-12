import os
from sqlalchemy import Column, ForeignKey, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

''' 
@EDIT: Database credentials handled using the dynamic environment variables 
'''
database_path = os.getenv('DATABASE_URL', "postgresql://postgres:1701@localhost:5432/agency")
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Club
Have name, category and asset
'''
class Club(db.Model):  
  __tablename__ = 'clubs'
  
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  category = Column(String)
  asset = Column(String)
  players = db.relationship('Player', back_populates='club')
  
  def __init__(self, name, category, asset):
    self.name = name
    self.category = category
    self.asset = asset

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'category': self.category,
      'asset': self.asset
    }

  def __repr__(self):
    return json.dumps(self.format())

'''
Player
Have name, value and club_id
'''
class Player(db.Model):  
  __tablename__ = 'players'
  
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  value = Column(String)
  club_id = Column(Integer, ForeignKey('clubs.id'))
  club = db.relationship('Club', back_populates='players')
  
  def __init__(self, name, value, club_id):
    self.name = name
    self.value = value
    self.club_id = club_id

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'value': self.value,
      'club_id': self.club_id
    }

  def __repr__(self):
    return json.dumps(self.format())