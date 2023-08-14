from dataclasses import dataclass

@dataclass
class PersonDto:
    apelido: str
    nome: str
    nascimento: str
    stack: str | None = None
