from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship , declarative_base
from werkzeug.security import generate_password_hash
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)  # Store hashed passwords

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String)
    added_by = Column(Integer, ForeignKey('users.id'))  # User who added the item
    user = relationship('User', back_populates='items')

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=datetime.datetime.utcnow)
    total_price = Column(Float, nullable=False)
    sold_by = Column(Integer, ForeignKey('users.id'))  # User who sold the item
    item = relationship('Item')
    user = relationship('User', back_populates='sales')

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    ticket_data = Column(String, nullable=False)
    sale = relationship('Sale')

User.items = relationship('Item', order_by=Item.id, back_populates='user')
User.sales = relationship('Sale', order_by=Sale.id, back_populates='user')

# Update this with your actual PostgreSQL database URL
DATABASE_URL = 'postgresql://postgres:1234@localhost/Store_DB'

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def create_default_admin():
    default_admin = session.query(User).filter_by(username='root').first()
    if not default_admin:
        hashed_password = generate_password_hash('1234')
        admin = User(username='root', password_hash=hashed_password)
        session.add(admin)
        session.commit()
        print("Default admin created.")

# Create the default admin user
create_default_admin()