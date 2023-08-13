from sqlalchemy import or_

from configs.database import database
from models import PersonModel


class PersonController:
    @classmethod
    def add_person(cls, nickname, name, birth, stack):
        if database.session.query(PersonModel).filter_by(nickname=nickname).one_or_none():
            raise TypeError("nickname is already in use")

        person = PersonModel(
            nickname=nickname,
            name=name,
            birth=birth,
            stack=stack,
        )

        person.validate()

        database.session.add(person)
        database.session.commit()

        return person
    
    @classmethod
    def get_person(cls, person_id):
        return database.session.query(PersonModel).filter_by(id=person_id).one_or_none()

    @classmethod
    def count_people(cls):
        return database.session.query(PersonModel).count()
    
    @classmethod
    def find_people(cls, search_term: str):
        return database.session.query(PersonModel).filter(
            or_(
                PersonModel.nickname.contains(search_term),
                PersonModel.name.contains(search_term),
                PersonModel.stack.contains(search_term),
            )
        ).limit(50)
