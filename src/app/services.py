from configs.database import connect_to_database
from app.models import Person


class PeopleServices:
    def create_person(self, person: Person) -> Person:
        person.prepare()
        connection = connect_to_database()
        cursor = connection.cursor()

        try:
            stack = ",".join(person.stack)
            cursor.execute(
                "INSERT INTO tb_people (id, apelido, nome, nascimento, stack, consulta) VALUES (%s, %s, %s, %s, %s, %s)",
                (person.id,  person.apelido, person.nome, person.nascimento, stack, person.consulta)
            )
            connection.commit()
            cursor.close()
            connection.close()
            return person

        except Exception as exc:
            connection.rollback()
            cursor.close()
            connection.close()
            raise exc

    def get_person(self, person_id: str) -> Person | None:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tb_people WHERE id = '%s'" % person_id)
        
        if person_data := cursor.fetchone():
            stack = person_data[4].split(",") if person_data[4] else []
            return Person(
                id=person_data[0],
                apelido=person_data[1],
                nome=person_data[2],
                nascimento=person_data[3],
                stack=stack,
                consulta=person_data[5],
            )

    def list_people(self, search_term: str) -> list[Person]:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tb_people WHERE lower(consulta) LIKE '%s' LIMIT 50" % f"%{search_term.lower()}%")
        
        person_data = cursor.fetchall()

        result = []

        for person in person_data:
            stack = person[4].split(",") if person[4] else []
            result.append(Person(
                id=person[0],
                apelido=person[1],
                nome=person[2],
                nascimento=person[3],
                stack=stack,
                consulta=person[5],
            ))

        return result
    
    def count_people(self) -> int:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT count(*) FROM tb_people")
        count = cursor.fetchone() or [0]

        return count[0]        
