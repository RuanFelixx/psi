from sqlalchemy.orm import Mapped, mapped_column
from database import db
class User(db.Model):
    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]

class livro(db.Model):
    __tablename__='livro'
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    autor: Mapped[str]