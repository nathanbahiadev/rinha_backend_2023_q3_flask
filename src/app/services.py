import json
import os

import psycopg2
from redis import Redis

from app.models import Person


def connect_to_database():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "postgres"),
        database=os.environ.get("POSTGRES_DB", "mydatabase"),
        user=os.environ.get("POSTGRES_USER", "myuser"),
        password=os.environ.get("POSTGRES_PASSWORD", "mypassword"),
    )


class PeopleServices:
    cache = Redis.from_url(os.environ.get("REDIS_URL", "redis://redis:6379"))

    def create_person(self, person: Person) -> Person:   
        if self.cache.get(person.apelido):
            raise TypeError("apelido is already in use")

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

            self.cache.set(person.id, person.model_dump_json(), 120) # type: ignore
            self.cache.set(person.apelido, "1")
            return person

        except Exception as exc:
            connection.rollback()
            cursor.close()
            connection.close()
            raise exc

    def get_person(self, person_id: str) -> Person | None:
        if cached_person := self.cache.get(person_id):
            person_data = json.loads(cached_person) # type: ignore
            return Person(
                id=person_data["id"],
                apelido=person_data["apelido"],
                nome=person_data["nome"],
                nascimento=person_data["nascimento"],
                stack=person_data["stack"],
                consulta=person_data["consulta"],
            )

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
