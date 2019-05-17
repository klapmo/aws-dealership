from sqlalchemy import create_engine,Column,String,Numeric,Integer,Date,ForeignKey # Create_Engine grabs AWS URL, Column is creating the column to hold, String allows us to use VARCHAR in our db 
from sqlalchemy.ext.declarative import declarative_base # See notes, saves time in creating classes to fill tables
from sqlalchemy.orm import sessionmaker,relationship # Line of communication between local machine and remote AWS db

db_string = "postgres://klapmo:codingtemple@dealership.c463ql7lyfat.us-east-2.rds.amazonaws.com:5432/dealership_project"

db = create_engine(db_string) # Creating the communication between local machine and AWS server instance
Base = declarative_base() # Setting it as a variable title Base for ease of use in calling declarative_base function - captial B denotes its a class we're using

# Creation of Database Models for Object Relational Mapper -- ORM
class Salesperson(Base): # Using the delcarative_base 
    __tablename__ = 'salesperson'
    salesperson_id = Column(Integer,primary_key = True)
    name = Column(String)
    invoice = relationship("Invoice", backref="salesperson")


class Customer(Base): # Using the delcarative_base 
    __tablename__ = 'customer'
    customer_id = Column(Integer,primary_key = True)
    name = Column(String)
    customer_car = relationship("CustomerCar", backref="customer")
    invoice = relationship("Invoice", backref="customer")


class Parts(Base): # Using the delcarative_base 
    __tablename__ = 'parts'
    parts_id = Column(Integer,primary_key = True)
    price = Column(Numeric(9,0))
    part_name = Column(String)
    service = relationship("Service", backref="parts")


class Inventory(Base): # Using the delcarative_base 
    __tablename__ = 'inventory'
    serial_number = Column(String,primary_key = True)
    price = Column(Numeric(9,0))
    invoice = relationship("Invoice", backref="inventory")


class Mechanics(Base): # Using the delcarative_base 
    __tablename__ = 'mechanics'
    mechanic_id = Column(Integer,primary_key = True)
    name = Column(String)
    service = relationship("Service", backref="mechanics")


class CustomerCar(Base): # Using the delcarative_base 
    __tablename__ = 'customer_car'
    serial_number = Column(String,primary_key = True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    service = relationship("Service", backref="customer_car")


class Invoice(Base): # Using the delcarative_base 
    __tablename__ = 'invoice'
    invoice_id = Column(Integer,primary_key = True)
    amount = Column(Numeric(9,0))
    invoice_date = Column(Date)
    serial_number = Column(String, ForeignKey('inventory.serial_number'))
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    salesperson_id = Column(Integer, ForeignKey('salesperson.salesperson_id'))

class Service(Base): # Using the delcarative_base 
    __tablename__ = 'service'
    service_id = Column(Integer,primary_key = True)
    price = Column(Numeric(9,0))
    serial_number = Column(String, ForeignKey('customer_car.serial_number'))
    mechanic_id = Column(Integer, ForeignKey('mechanics.mechanic_id'))
    parts_id = Column(Integer, ForeignKey('parts.parts_id'))
    service_ticket = relationship("ServiceTicket", backref="service")


class ServiceTicket(Base): # Using the delcarative_base 
    __tablename__ = 'service_ticket'
    service_ticket_id = Column(Integer,primary_key = True)
    service_id = Column(Integer, ForeignKey('service.service_id'))
    service_date = Column(Date)


class Records(Base): # Using the delcarative_base 
    __tablename__ = 'records'
    record_id = Column(Integer,primary_key = True)
    invoice_id = Column(Integer, ForeignKey('invoice.invoice_id'))


Session = sessionmaker(db)
create_session = Session()

Base.metadata.create_all(db) # Takes all data associated with Base classes and pushes to AWS

customer = Customer(name="david")
create_session.add(customer)
create_session.commit()

customers = create_session.query(Customer)
for cust in customers:
    print(customer.name)
# # Create first film table
# customer1 = Customer(title='Doctor Strange',director='Scott Derrickson',year='2016') # Creates values for first entry
# create_session.add(doctor_strange) # Adds data to a new db session
# create_session.commit() # Pushes added data to AWS

# films = create_session.query(Film)
# for film in films:
#     print(film.title)
