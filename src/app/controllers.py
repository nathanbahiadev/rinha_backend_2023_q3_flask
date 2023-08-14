import json

from typing import Any
from uuid import uuid4

from configs.database import connect_to_database
from services.cache import RedisCache
from app.entities import Person
from app.factories import PersonFactory
from app.dtos import PersonDto


class DatabasePeople:
    def create_person(self, person_dto: PersonDto) -> Person:
        person = Person(
            id=str(uuid4()),
            apelido=person_dto.apelido,
            nome=person_dto.nome,
            nascimento=person_dto.nascimento,
            stack=person_dto.stack
        )

        connection = connect_to_database()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO tb_people (id, apelido, nome, nascimento, stack, consulta) VALUES (%s, %s, %s, %s, %s, %s)",
                (person.id,  person.apelido, person.nome, person.nascimento, person.stack, person.consulta)
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

        cursor.execute("SELECT * FROM tb_people WHERE id = %s", person_id)
        
        if person_data := cursor.fetchone():
            return PersonFactory.from_db(person_data)

    def list_people(self, search_term: str) -> list[Person]:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM tb_people WHERE lower(consulta) LIKE %{search_term.lower()}% LIMIT 50")
        person_data = cursor.fetchall()

        return [PersonFactory.from_db(data) for data in person_data]
    
    def count_people(self) -> int:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT count(*) FROM tb_people")
        count = cursor.fetchone() or [0]

        return count[0]        


class CachePeople:
    cache = RedisCache()

    @classmethod
    def get(cls, person_id: str) -> Person | None:
        if person_data := cls.cache.get(person_id):
            return PersonFactory.from_json(person_data)

    @classmethod
    def set(cls, key: str, person_data: Any) -> None:
        cls.cache.set(key, json.dumps(person_data))


class PersonController:
    database_controller = DatabasePeople()
    cache_controller = CachePeople()

    @classmethod
    def add_person(cls, person_dto: PersonDto) -> Person:
        if cls.cache_controller.get(person_dto.apelido):
            raise TypeError("apelido is already in use")
        
        person = cls.database_controller.create_person(person_dto)
        cls.cache_controller.set(person.apelido, PersonFactory.to_json(person))
        cls.cache_controller.set(person.id, person.apelido)
        return person

    @classmethod
    def get_person(cls, person_id) -> Person | None:
        if person := cls.cache_controller.get(person_id):
            return person
        
        if person := cls.database_controller.get_person(person_id):
            cls.cache_controller.set(person.apelido, PersonFactory.to_json(person))
            cls.cache_controller.set(person.id, person.apelido)
            return person

    @classmethod
    def find_people(cls, search_term: str) -> list[Person]:
        return cls.database_controller.list_people(search_term)

    @classmethod
    def count_people(cls) -> int:
        return cls.database_controller.count_people()
