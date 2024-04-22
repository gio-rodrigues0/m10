from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database.database import db
from sqlalchemy.sql import func

class User(db.Model):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False)
  password = Column(String(50), nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, name:{self.name}, email:{self.email}, password:{self.password}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "email": self.email,
      "password": self.password}
  
class Tasks(db.Model):
  __tablename__ = 'tasks'

  id = Column(Integer, primary_key=True, autoincrement=True)
  description = Column(String(50), nullable=False)
  timestamp = Column(DateTime, default=func.now())

  def __repr__(self):
    return f'<Tasks:[id:{self.id}, description:{self.description}, timestamp:{self.timestamp}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "description": self.description,
      "timestamp": self.timestamp}