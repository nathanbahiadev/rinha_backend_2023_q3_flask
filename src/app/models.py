from datetime import date
from typing import List
from uuid import uuid4, UUID as _UUID

from pydantic import BaseModel, constr
from sqlalchemy import Column, UUID, Date, ARRAY, String

from app.database import db


class PersonModel(db.Model):
    __tablename__ = "tb_people"

    id = Column(UUID, primary_key=True, unique=True)
    consulta = Column(String)
    apelido = Column(String(32), unique=True, index=True)
    nome = Column(String(100))
    nascimento = Column(Date)
    stack = Column(ARRAY(String(32)), nullable=True)


class Person(BaseModel):
    id: _UUID = uuid4()
    consulta: str | None = None
    apelido: constr(max_length=32) # type: ignore
    nome: constr(max_length=100) # type: ignore
    nascimento: date # type: ignore
    stack: List[constr(max_length=32)] # type: ignore

    class Config:
        from_attributes = True


class ListPeople(BaseModel):
    people: List[Person]
