from flask import Blueprint, request, make_response

from app.controllers import PersonController
from app.dtos import PersonDto
from app.factories import PersonFactory

person_bp = Blueprint("person", __name__, url_prefix="/")
person_controller = PersonController()


@person_bp.post("pessoas")
def add_people():
    try:
        person = person_controller.add_person(PersonDto(**(request.json or {})))

        response = make_response(PersonFactory.to_json(person), 201)
        response.headers["Location"] = f"/pessoas/{person.id}"
        return response
    
    except TypeError as e:
        return make_response({"error_type": "ValidationError", "error_message": str(e)}, 422)
    
    except Exception as e:
        return make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)


@person_bp.get("pessoas/<person_id>")
def get_people(person_id):
    try:
        if person := person_controller.get_person(person_id):
            return make_response(PersonFactory.to_json(person), 200)
        
        return make_response({"error_type": "NotFound", "error_message": "Resource not found"}, 404)
    
    except Exception as e:
        return  make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)


@person_bp.get("pessoas/")
def find_people():
    try:
        if search_term := request.args.get("t", ""):
            people = person_controller.find_people(search_term)
            return make_response([PersonFactory.to_json(p) for p in people], 200)
        
        return make_response({"error_type": "BadRequest", "error_message": "Query string 't' must be provided"}, 400)
        
    except Exception as e:
        return make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)


@person_bp.get("contagem-pessoas/")
def count_people():
    try:
        count = person_controller.count_people()
        return str(count)
    
    except Exception as e:
        return make_response({"error_type": e.__class__.__name__, "error_message": str(e)}, 500)
   