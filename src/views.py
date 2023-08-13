from flask import Blueprint, request, make_response

from controllers import PersonController

person_bp = Blueprint("person", __name__, url_prefix="/")


@person_bp.post("pessoas")
def add_people():
    data = request.json or {}
    person_controller = PersonController()

    try:
        person = person_controller.add_person(
            nickname=data.get("apelido", ""),
            name=data.get("nome", ""),
            birth=data.get("nascimento", ""),
            stack=data.get("stack")
        )

        response = make_response(person.to_json(), 201)

        response.headers["Location"] = f"/pessoas/{person.id}"

        return response
    
    except TypeError as e:
        return make_response({
            "error_type": "ValidationError",
            "error_message": str(e)
        }, 422)
    
    except Exception as e:
        return make_response({
            "error_type": e.__class__.__name__,
            "error_message": str(e)
        }, 500)


@person_bp.get("pessoas/<uuid:person_id>")
def get_people(person_id):
    person_controller = PersonController()

    try:
        if person := person_controller.get_person(person_id):
            return make_response(person.to_json(), 200)
        
        return make_response({
            "error_type": "NotFound",
            "error_message": "Resource not found"
        }, 404)
    
    except Exception as e:
        return make_response({
            "error_type": e.__class__.__name__,
            "error_message": str(e)
        }, 500)


@person_bp.get("pessoas")
def find_people():
    search_term = request.args.get("t", "")
    person_controller = PersonController()

    try:
        people = person_controller.find_people(search_term)
        return make_response([p.to_json() for p in people], 200)
    
    except Exception as e:
        return make_response({
            "error_type": e.__class__.__name__,
            "error_message": str(e)
        }, 500)


@person_bp.get("contagem-pessoas")
def count_people():
    person_controller = PersonController()

    try:
        count = person_controller.count_people()
        return str(count)
    
    except Exception as e:
        return make_response({
            "error_type": e.__class__.__name__,
            "error_message": str(e)
        }, 500)
   