from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    id: str
    apelido: str
    nome: str
    nascimento: str
    stack: str | None = None
    consulta: str | None = None

    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if not self.apelido or len(self.apelido) > 32:
            raise TypeError("apelido is a required field and must be 32 characters or less")
        
        if not self.nome or len(self.nome) > 100:
            raise TypeError("nome is a required field and must be 100 characters or less")
        
        if not self.nascimento:
            raise TypeError("nascimento is a required field")
        
        try:
            datetime.strptime(self.nascimento, "%Y-%m-%d")
        except ValueError:
            raise TypeError("nascimento must be a valid date")
        
        if self.stack:
            if not isinstance(self.stack, list):
                raise TypeError("stack must be an array")
            
            for stack in self.stack:
                if len(stack) > 32:
                    raise TypeError("stack nome must be 32 characters or less")

        self.stack = ",".join(self.stack or [])
        self.consulta = f"{self.apelido},{self.nome},{self.stack}".lower()
