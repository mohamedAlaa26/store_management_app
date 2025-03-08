from sqlalchemy import create_engine
from models import Base


DATABASE_URL = 'postgresql://postgres:1234@localhost/Store_DB'

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
print("Tables created successfully")
