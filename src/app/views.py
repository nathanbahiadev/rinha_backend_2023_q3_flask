from flask import Blueprint, request, make_response
from psycopg2.errors import UniqueViolation

from app.services import PeopleServices
from app.models import Person


person_bp = Blueprint("person", __name__, url_prefix="/")
services = PeopleServices()


@person_bp.post("pessoas")
def add_people():
    try:
        json_data = request.json or {}
        
        if not json_data:
            return make_response({"error_type": "ValidationError", "error_message": "Invalid payload"}, 422)

        person = services.create_person(Person.model_validate(json_data))
        response = make_response(person.model_dump(), 201)
        response.headers["Location"] = f"/pessoas/{person.id}"
        return response
    
    except (TypeError, UniqueViolation) as e:
        return make_response({"error_type": "ValidationError", "error_message": str(e)}, 422)
    
    except Exception as e:
        return make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)


@person_bp.get("pessoas/<person_id>")
def get_people(person_id):
    try:
        if person := services.get_person(person_id):
            return make_response(person.model_dump(), 200)
        
        return make_response({"error_type": "NotFound", "error_message": "Resource not found"}, 404)
    
    except Exception as e:
        return  make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)


@person_bp.get("pessoas/")
def find_people():
    try:
        search_term = request.args.get("t", "")
        if not search_term:
            return make_response({"error_type": "BadRequest", "error_message": "Query string 't' must be provided"}, 400)

        people = services.list_people(search_term)
        response = [person.model_dump_json() for person in people]
        return make_response(response, 200)
        
    except Exception as e:
        return make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)


@person_bp.get("contagem-pessoas/")
def count_people():
    try:
        count = services.count_people()
        return str(count)
    
    except Exception as e:
        return make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)
   