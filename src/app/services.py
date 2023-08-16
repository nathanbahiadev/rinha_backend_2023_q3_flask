from app.models import Person, PersonModel
from app.database import db


class PeopleServices:
    def create_person(self, person: Person) -> Person:   
        try:
            person.consulta = f"{person.apelido},{person.nome},{person.stack}"
            db.session.add(PersonModel(**person.model_dump()))
            db.session.commit()
            return person
        
        except Exception as exc:
            raise exc

    def get_person(self, person_id: str) -> Person | None:
        if person := db.session.query(PersonModel).filter_by(id=person_id).one_or_none():
            return Person.from_orm(person)

    def list_people(self, search_term: str) -> list[Person]:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tb_people WHERE lower(consulta) LIKE '%s' LIMIT 50" % f"%{search_term.lower()}%")
        
        person_data = cursor.fetchall()
        result = []

        for person in person_data:
            result.append(Person(
                id=person[0],
                apelido=person[1],
                nome=person[2],
                nascimento=person[3],
                stack=person[4],
                consulta=person[5],
            ))

        return result
    
    def count_people(self) -> int:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT count(*) FROM tb_people")
        count = cursor.fetchone() or [0]

        return count[0]        
