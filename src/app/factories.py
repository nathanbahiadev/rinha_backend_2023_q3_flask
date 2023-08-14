from app.entities import Person


class PersonFactory:
    @classmethod
    def to_json(cls, person: Person):
        return {
            "id": person.id,
            "nome": person.nome,
            "apelido": person.apelido,
            "nascimento": person.nascimento,
            "stack": person.stack.split(",") if person.stack else None,
        }
    
    @classmethod
    def from_json(cls, person_data: dict):
        return Person(
            id=person_data["id"],
            apelido=person_data["apelido"],
            nome=person_data["nome"],
            nascimento=person_data["nascimento"],
            stack=person_data["stack"]
        )

    @classmethod
    def from_db(cls, row: tuple):
        return Person(
            id=row[0],
            apelido=row[1],
            nome=row[2],
            nascimento=row[3],
            stack=row[4]
        )
