from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import relationship
from typing import list

engine = create_engine('sqlite:///exemplo01.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base): 
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    generate_id:Mapped[int]=mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )
    gerenciados:Mapped[list['User']] = relationship('User')
    def __repr__(self) -> str:
        return self.nome

Base.metadata.create_all(bind=engine)

user1 = User(nome='João')
session.add(user1)
session.commit()

user2 = User(nome='Davi', gerent_id=1)

user3 = User(nome='Ítalo', gerent_id=1)

user4 = User(nome='Hiandro')

session.add_all([user2,user2,user4])
session.commit()


sql = select(User).where(User.id == 1)
chefe = session.execute(sql).scalars().first()
print(chefe.nome)

print(chefe.gerenciados)