from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Table, Column, ForeignKey
from typing import List
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///exemplo2.db')
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
    curso_id:Mapped[int] = mapped_column(ForeignKey('courses.id'), nullable=True)
    def __repr__(self) -> str:
        return f"Estudante={self.nome}"


class Curso(Base):
    __tablename__ = 'courses'
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    estudantes:Mapped[List['Estudante']] = relationship('Estudante',backref='curso')
    def __repr__(self) -> str:
        return f"Curso={self.nome}"

Base.metadata.create_all(bind=engine)

info = Curso(nome='informatica')

x = Estudante(nome='jão', Curso_id=1)
y = Estudante(nome='Davi', Curso_id=1)
z = Estudante(nome='Seboso',Curso_id=1)

#session.add(info)
#session.add_all([x,y,z])
#session.commit()

curso = session.query(Curso, 1).get()
print(curso)
print(curso.estudantes)

estudante = session.query(Estudante).get(1)
print(str(estudante) + 'estuda' + str(estudante.curso))