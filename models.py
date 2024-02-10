from sqlalchemy import Boolean, Column, Integer, String,DateTime,Date
from datetime import date
from database import Base

class User(Base):
    __tablename__="Customers"

    firstname=Column(String(50))
    lastname= Column(String(50)) 
    # phone=Column(Integer,unique=True, primary_key=True)
    dob=Column(Date)
    email=Column(String(50),unique=True,primary_key=True)
    address=Column(String(100))


