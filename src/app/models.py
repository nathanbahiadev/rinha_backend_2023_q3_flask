from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, constr, validator


class Person(BaseModel):
    id: str | None = None
    consulta: str | None = None
    apelido: constr(max_length=32) # type: ignore
    nome: constr(max_length=100) # type: ignore
    nascimento: constr(max_length=10) # type: ignore
    stack: List[constr(max_length=32)] # type: ignore

    def prepare(self):
        self.id = str(uuid4())
        self.consulta = f"{self.apelido},{self.nome},{self.stack}".lower()        

    @validator('nascimento')
    def validate_nascimento(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError("nascimento must be a valid date")


class ListPeople(BaseModel):
    people: List[Person]
