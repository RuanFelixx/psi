from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models import Base, User
from faker import Faker

engine = create_engine("sqlite:///test.db")
session = Session(bind=engine)

def start_db():
    Base.metadata.create_all(bind=engine)
    
    gerador_faker = Faker()

    for _ in range(100):
        fake_name = gerador_faker.unique.name()
        user = User(name=fake_name)
        session.add(user)

    session.commit()

def destroy_db():
    Base.metadata.drop_all(bind=engine)

