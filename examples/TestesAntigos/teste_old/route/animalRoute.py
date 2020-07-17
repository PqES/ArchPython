from flask import Blueprint, Flask, jsonify, request
from animalController import CtrlAnimal


app_animal = Blueprint('animal', __name__)


@app_animal.route('/animal', methods=['GET'])
def create_animal_render():
    return CtrlAnimal().render_page()

@app_animal.route('/api/animal', methods=['POST'])
def create_animal():
    data = request.get_json()
    print(request)
    print("aa")
    print(data)
    new_animal = CtrlAnimal().create_animal(data)

    return jsonify(
        status=200,
        data=new_Animal)