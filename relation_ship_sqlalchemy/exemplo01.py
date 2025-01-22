from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from typing import List

engine = create_engine('sqlite:///exemplo1.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

students_courses = Table(
    'students_courses',
    Base.metadata,
    Column('students_id', ForeignKey('Estudante.id'),primary_key=True),
    Column('courses_id', ForeignKey('Curso_id'),primary_key=True)
)

class Estudante(Base):
    __tablename__ = 'students'
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    cursos:Mapped[List['Curso']] = relationship(
        'Curso', 
        secondary=students_courses,
        back_populates='estudantes')

class Curso(Base):
    __tablename__ = 'courses'
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    estudantes = relationship('Estudante', back_populates='cursos')

Base.metadata.create_all(bind=engine)

info = Curso(nome='informatica')

x = Estudante(nome='jão', Curso_id=1)
y = Estudante(nome='Davi', Curso_id=1)
z = Estudante(nome='Seboso',Curso_id=1)

session.add(info)
session.add_all([x,y,z])
session.commit()

info = session.query(Curso).get(1)
info.estudantes.append(x)
session.commit()

info.estudantes.remove(x)
session.commit()